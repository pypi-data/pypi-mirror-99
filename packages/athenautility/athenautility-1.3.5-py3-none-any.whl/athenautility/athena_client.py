#!/usr/bin/env python
import json
import os
import logging
import requests
import pandas as pd
from IPython.display import display, HTML

logger = logging.getLogger(__name__)

STATUS = "status"
RESULT = "result"
ERROR = "error"
SUCCESS = "SUCCESS"
FAILED = "FAILED"

################################################################################
# Queries
################################################################################

QUERY_SHOW_DATABASES = """show databases;"""
QUERY_SHOW_TABLES = """show tables in {schema_name};"""
QUERY_TABLE_RECORDS_WITH_LIMIT = """select * from {schema_name}.{table_name} limit {limit};"""
QUERY_TABLE_RECORDS = """select * from {schema_name}.{table_name} limit 100;"""

# Athena services
API_VALIDATE_USER = "/ccf/services/v2.0/validate_user"
API_GET_ATHENA_DATABASES = "/ccf/services/v2.0/get_athena_databases"
API_GET_ATHENA_TABLES = "/ccf/services/v2.0/get_athena_tables"
API_QUERY_ATHENA_TABLE = "/ccf/services/v2.0/query_athena_table"
API_RUN_QUERY_ON_ATHENA = "/ccf/services/v2.0/run_query_on_athena"

HEADERS = {
    'content-type': "application/json",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36"
}


################################################################################
# Athena Client
################################################################################

class AthenaClient:
    # Environment Variables
    _USER_NAME: str = 'USER_NAME'
    _ACCESS_TOKEN: str = 'ACCESS_TOKEN'
    _USER_ROLE: str = 'USER_ROLE'
    _CCF_SERVICES_HOST: str = 'CCF_SERVICES_HOST'

    def __init__(self):
        self._user_name = os.getenv(self._USER_NAME, None)
        self._access_token = os.getenv(self._ACCESS_TOKEN, None)
        self._user_role = os.getenv(self._USER_ROLE, None)
        self._ccf_services_host = os.getenv(self._CCF_SERVICES_HOST, None)

    def connect(self):
        # TODO - Add user validation
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role})
            r = requests.post(self._ccf_services_host + API_VALIDATE_USER, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException:
            raise Exception("RequestException occurred") from None

    def databases(self, result_as_df=True):
        """Returns all the schemas available in Athena"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role})
            r = requests.post(self._ccf_services_host + API_GET_ATHENA_DATABASES, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if result_as_df and isinstance(response[RESULT], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption("Databases").hide_index()
                    # return HTML(response_as_df.to_html(index=False))
                    return display(response_as_df)
                else:
                    return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException:
            raise Exception("RequestException occurred") from None

    def tables(self, schema_name, result_as_df=True):
        """Returns all the tables present in a schema"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role, "schema_name": schema_name})
            r = requests.post(self._ccf_services_host + API_GET_ATHENA_TABLES, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if result_as_df and isinstance(response[RESULT], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(f'Tables in schema: {schema_name}').hide_index()
                    # return HTML(response_as_df.to_html(index=False))
                    return display(response_as_df)
                else:
                    return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException:
            raise Exception("RequestException occurred") from None

    def top(self, schema_name, table_name, limit=None, result_as_df=True):
        """Returns records from a table"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role, "schema_name": schema_name,
                                  "table_name": table_name, "limit": limit})
            r = requests.post(self._ccf_services_host + API_QUERY_ATHENA_TABLE, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if result_as_df and isinstance(response[RESULT], (dict, list)):
                    # results = [pd.DataFrame.from_dict(i).to_html(index=False) for i in response[RESULT]]
                    # combined_results = ''.join(results)
                    table_header = f'Top {limit} records of table {schema_name}.{table_name}' if limit else f'Top 100 records of table {schema_name}.{table_name}'
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(
                        table_header).hide_index()
                    return display(response_as_df)
                else:
                    return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException:
            raise Exception("RequestException occurred") from None

    def run_query(self, query_string, result_as_df=True):
        """Run a specified query"""
        try:
            payload = json.dumps(
                {"user_name": self._user_name, "role_id": self._user_role, "query_string": query_string})
            r = requests.post(self._ccf_services_host + API_RUN_QUERY_ON_ATHENA, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if result_as_df and isinstance(response[RESULT], (dict, list)):
                    queries = query_string.split(';')
                    results = [pd.DataFrame.from_dict(item).style.set_caption(f"""Query results for \"{queries[i]};\"""").hide_index() for i, item in enumerate(response[RESULT])]
                    # combined_results = ''.join(results)
                    # return HTML(combined_results)
                    display(*results)
                else:
                    return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException:
            raise Exception("RequestException occurred") from None
