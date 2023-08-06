"""
    SalesforceInteraction
"""

import ast
import json
import os
import requests
import traceback
from time import sleep
from datetime import datetime

from salesforce_bulk import SalesforceBulk
from salesforce_bulk.salesforce_bulk import BulkApiError
from simple_salesforce import Salesforce, SalesforceError
from salesforce_bulk.util import IteratorBytesIO

from datacoco_cloud.s3_interaction import S3Interaction
from datacoco_core.config import config
from datacoco_redis_tools.redis_tools import RedisInteraction
from datacoco_core.logger import Logger

# quick port from old coco for upload to fix engage sub in squidward
SALESFORCE_UPLOAD_URL = "https://{}/services/data/v29.0/sobjects/{}/"

LOG = Logger()

def parse_sf_records(nested_dict):
    """Recursively parse the nested dictionaries returned by Salesforce Simple API library,

    :param nested_dict: Nested dictionary object
    :return: Flattened dictionary representing record
    """
    for k, v in list(nested_dict.items()):
        if k == "attributes":
            nested_dict.pop(k)
        elif isinstance(v, dict):
            clean_dict = parse_sf_records(v)

            for child_key, clean_value in list(clean_dict.items()):
                clean_key = "{}.{}".format(k, child_key)
                nested_dict[clean_key] = clean_value

            nested_dict.pop(k)

    return nested_dict


def make_default_salesforce(project_id='datacoco3.db'):
    """
    :param project_id: to identify project source api calls
    """
    uat = config["salesforce"]["uat"]
    uat = True if uat == "True" else False

    salesforce = Salesforce(
        username=config["salesforce"]["username"],
        password=config["salesforce"]["password"],
        security_token=config["salesforce"]["token"],
        sandbox=uat,
        client_id=project_id
    )
    return salesforce


def make_request_header(session_id):
    request_header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % session_id,
    }
    return request_header


def upload_data_to_salesforce(table, upload_data, salesforce=None):
    if salesforce is None:
        salesforce = make_default_salesforce()

    url = SALESFORCE_UPLOAD_URL.format(salesforce.sf_instance, table)
    response = requests.post(
        url,
        headers=make_request_header(salesforce.session_id),
        data=json.dumps(upload_data),
    )
    response.raise_for_status()
    return response


class SFInteraction(object):
    """Simple class that interacts with Salesforce"""

    def __init__(self, username, password, token, uat, project_id='datacoco3.db', session_id=None, instance=None, version=None):
        """Instantiate a Salesforce interaction manager.

        UAT mode is explicitly set to a boolean value in case a string is provided.

        If Salesforce session credentials do not exist, attempt to retrieve.

        :param username: Username
        :param password: Password
        :param token: API token
        :param uat: Whether or not in UAT mode
        :param project_id: to identify project source api calls
        :param session_id:  Access token for existing session
        :param instance: Domain of Salesforce instance
        """
        if not username or not password or not token or uat is None:
            raise RuntimeError("%s request all __init__ arguments" % __name__)

        self.username = username
        self.password = password
        self.token = token
        self.session_id = session_id
        self.instance = instance
        self.project_id = project_id
        self.version = version

        self.conn = None
        self.bulk = None
        self.job_id = None
        self.batch_max_attempts = None
        self.batch_timeout = None
        self.batch_sleep_interval = None
        self.temp_file = "sf_temp_results.txt"

        self.redis_conn = None
        self.session_credentials_key = "sf_session_credentials"

        # Handle string uat which should be boolean
        if isinstance(uat, str) and uat.lower() in ("true", "t"):
            self.uat = True
        else:
            self.uat = False

        # Retrieve session_id and/or instance if they do not exist
        if not self.session_id or not self.instance:
            self._get_session_credentials()

    def connect(self):
        """Connect to the Salesforce API client.

        Only executes if there is not an existing open Salesforce connection.

        If there are a session_id and an instance, attempt to connect to
        the existing session. The existing session connection is verified with a Salesforce API describe call.

        If that fails, create a new connection.

        There are 3 retry attempts
        """
        if self.session_id and self.instance:
            retry_count = 1
            while True:
                if retry_count > 3:
                    LOG.l("Could not connect to Salesforce in the specified number of retries.")
                    LOG.l("Starting a new connection...")
                    break
                else:
                    LOG.l(f"Connecting to Salesforce: attempt {retry_count} of 3...")

                try:
                    self.conn = Salesforce(
                        session_id=self.session_id, instance=self.instance, client_id=self.project_id, version=self.version
                    )
                    self.conn.describe()  # Connection health check
                    return #Sucess, leave this function
                except SalesforceError as sfe:
                    LOG.l(f"Encountered error connecting to Salesforce:\n{sfe}")
                    retry_count += 1
                    sleep(5)
                    continue


        #If reconnecting didn't work or session_id is not set, then start a new connection
        try:
            self._create_new_connection()
        except:
            raise Exception("Could not initiate connection to Salesforce!")



    def fetch_soql(
        self,
        db_table,
        soql,
        batch=True,
        batch_timeout=600,
        batch_sleep_int=10,
        batch_max_attempts=1,
    ):
        """Fetch results from Salesforce soql queries.

        Batch Salesforce queries results saved to a file and retrieved because they are in CSV format
        and to avoid bulk queries timeouts.

        :param db_table: Database table name
        :param soql: Soql queries
        :param batch: Whether to use Salesforce Batch or Simple API
        :param batch_sleep_int: Salesforce Bulk query sleep interval
        :param batch_timeout: Batch job timeout in seconds
        :param batch_max_attempts: Maximum number of batch query creation attempts
        :return: If success, List of result dictionaries; Else empty list
        """
        try:
            if batch:
                # Set batch operation attributes
                self.batch_timeout = batch_timeout
                self.batch_sleep_interval = batch_sleep_int
                self.batch_max_attempts = batch_max_attempts

                results = self.get_query_records_dict(db_table, soql)

                # save to and read from file to avoid connection timeout
                self._save_results_to_file(results)
                records = self._get_results_from_file()
            else:
                result = self.conn.query(soql)

                # if there isn't a result return an empty list
                if result["records"]:
                    salesforce_records = json.loads(json.dumps(result["records"][0]))
                    parsed_records = parse_sf_records(salesforce_records)
                    records = [
                        parsed_records
                    ]  # put result in a list object for consistency
                else:
                    records = []
        except BulkApiError as e:
            self.bulk.abort_job(self.job_id)
            # TODO Handle failed bulk API transaction better
            raise e

        return records

    def get(self, object_name: str, object_id: str):
        """
        To get a dictionary with all the information regarding that record
        """
        return self.conn.__getattr__(object_name).get(object_id)

    def get_by_custom_id(self, object_name: str, field: str, id: str):
        """
        To get a dictionary with all the information regarding that record
        using a **custom** field that was defined as External ID:
        """
        return self.conn.__getattr__(object_name).get_by_custom_id(field, id)

    def upsert(self, object_name: str, field: str, id: str, data: dict):
        """
        To insert or update (upsert) a record using an external ID
        """
        return self.conn.__getattr__(object_name).upsert(f'{field}/{id}', data)

    def get_query_records_dict(self, db_table, soql_query):
        """Execute bulk Salesforce soql queries and return results as generator of dictionaries.

        :param db_table: Database table name
        :param soql_query: Soql queries
        :return: If success, List of result record dictionaries; Else empty list
        """
        self.bulk = SalesforceBulk(sessionId=self.session_id, host=self.instance)
        job = self.bulk.create_query_job(db_table, contentType="JSON")
        batch = self.bulk.query(job, soql_query)
        self.bulk.close_job(job)
        while not self.bulk.is_batch_done(batch):
            print("Waiting for batch query to complete")
            sleep(10)

        dict_records = []
        rec_count = 0
        print("Iterating through batch result set")
        for result in self.bulk.get_all_results_for_query_batch(batch):
            result = json.load(IteratorBytesIO(result))
            for row in result:
                rec_count += 1
                dict_records.append(row)
            print("Current fetched record count: ", rec_count)

        return dict_records

    def batch_query_records_dict(self, db_table, soql_query, concurrency='Serial'):
        """Execute bulk Salesforce soql queries and return results as generator of dictionaries.

        works only for PK CHUNKING enabled SF tables.

        Allows millions of record read.

        :param db_table: Database table name
        :param soql_query: Soql queries
        :return: If success, List of result record dictionaries; Else empty list
        """
        self.bulk = SalesforceBulk(sessionId=self.session_id, host=self.instance)
        job = self.bulk.create_query_job(db_table, contentType="JSON", pk_chunking=True, concurrency=concurrency)
        try:
            batch = self.bulk.query(job, soql_query)
            batch_list = self.bulk.get_batch_list(job)
            print('first batch', batch_list[0])
            batch_id = batch_list[0]['id']
            job_id = batch_list[0]['jobId']
            state = batch_list[0]['state']
            while state == 'Queued' or state == 'InProgress':
                print("Waiting for batch state Queued or InProgress to change " + state)
                sleep(10)
                state = self.bulk.batch_state(batch_id, job_id)

            batch_list = self.bulk.get_batch_list(job)
            print(f'number of batches: {len(batch_list)}')
            for item in batch_list:
                print('item', item)
                batch_id = item['id']
                job_id = item['jobId']
                state = item['state']

                if state == 'NotProcessed':
                    continue

                while not self.bulk.is_batch_done(batch_id, job_id):
                    print(f"Waiting for batch query to complete batch_id:{batch_id}, job_id: {job_id}, state: {state}")
                    sleep(10)
                    state = self.bulk.batch_state(batch_id, job_id)

                total_retry_count = len(batch_list)
                retry = len(batch_list)
                lastIndex = 0
                while retry > 0:
                    print(f'retry {retry} times left')
                    try:
                        for result in list(self.bulk.get_all_results_for_query_batch(batch_id, job_id))[lastIndex:]:
                            result = json.load(IteratorBytesIO(result))
                            lastIndex += 1
                            yield result
                        break
                    except requests.exceptions.ChunkedEncodingError as e:
                        print('Chunking failed')
                        retry -= 1
                        self.connect()
                        self.bulk = SalesforceBulk(sessionId=self.session_id, host=self.instance)
                        pass
                    except Exception as e:
                        print('There was an error')
                        traceback.print_exc()
                        retry -= 1
                        self.connect()
                        self.bulk = SalesforceBulk(sessionId=self.session_id, host=self.instance)
                        pass
                if retry <= 0:
                    raise Exception(f'Retried {total_retry_count} times and it still failed')
        except BulkApiError as e:
            self.bulk.abort_job(self.job_id)
            raise e

    def upload_records_to_s3(
        self, records, s3_bucket, s3_key, aws_access_key, aws_secret_key
    ):
        """Upload records to s3.

        :param records: Records filename
        """
        self._save_results_to_file(records)
        datetime_today = datetime.today().strftime("%Y-%m-%d-%X")

        s3_dest_key = s3_key + datetime_today

        s3_interaction = S3Interaction(aws_access_key, aws_secret_key)
        s3_interaction.put_file_to_s3(s3_bucket, s3_dest_key, self.temp_file)

        return s3_dest_key

    def get_description(self, object_name):
        """Retrieves object description

        :param object_name: Salesforce object/table name
        """
        retry = True
        while retry:
            try:
                return self.conn.__getattr__(object_name).describe()
            except SalesforceError as sfe:
                retry = self._sf_except_reconnect(sfe)


    def _sf_except_reconnect(self, e):
        """ Used in try/catch blocks to reinit the connection

        returns true if the code should be retried, false if no connection could be made
        """
        LOG.l(f"Encountered error:\n{e}")
        try:
            self.connect()
            return True
        except Exception:
            return False


    def _create_new_connection(self):
        """Create a new Salesforce API client connection.

        After the connection is created, the Salesforce session credentials are stored externally.
        """
        self.conn = Salesforce(
            username=self.username,
            password=self.password,
            security_token=self.token,
            sandbox=self.uat,
            client_id=self.project_id
        )
        self.session_id = str(self.conn.session_id)
        self.instance = str(self.conn.sf_instance)
        self._set_session_credentials()

    def _save_results_to_file(self, records):
        """Save Salesforce Bulk API results to a temp file.

        :param records: Records to save
        """
        with open(self.temp_file, "w") as f:
            for r in records:
                f.write("\n")
                f.write(str(str(r).encode("utf-8")))

    def _get_results_from_file(self):
        """Get Salesforce Bulk API results from a temp file.

        The records must be parsed. After the results are retrieved. The file is deleted.

        :return: Iterator with records.
        """
        results = []
        with open(self.temp_file, "r") as f:
            records = f.read()[1:].splitlines()
            for r in records:
                r = ast.literal_eval(r)
                results.append(r)
        os.remove(self.temp_file)
        return results

    def _get_session_credentials(self):
        """Get Salesforce session credentials stored in Redis.

        If the credentials variables do not exist, set the credentials as None.
        """
        # Establish connection to Redis
        self._connect_to_redis()
        # Get salesforce credentials if exists
        if self.redis_conn.conn.exists(self.session_credentials_key):
            self.session_id = self.redis_conn.fetch_by_key_name(
                self.session_credentials_key, "session_id"
            )
            self.instance = self.redis_conn.fetch_by_key_name(
                self.session_credentials_key, "instance"
            )
        else:
            self.session_id = None
            self.instance = None

    def _set_session_credentials(self):
        """Set Salesforce session credentials in Redis.

        """
        sf_session_credentials = {
            "session_id": self.session_id,
            "instance": self.instance,
        }
        self.redis_conn.set_key(self.session_credentials_key, sf_session_credentials)

    def _connect_to_redis(self):
        """Connect to Redis.

        """
        CONF = config()
        host = CONF["redis"]["server"]
        port = CONF["redis"]["port"]
        db = CONF["redis"]["db"]
        self.redis_conn = RedisInteraction(host, port, db)
        self.redis_conn.connect()
