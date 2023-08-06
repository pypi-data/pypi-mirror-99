#!/usr/bin/env python
import json
import sys
import logging
import requests
import socket
import pandas as pd

sys.tracebacklimit = None

logger = logging.getLogger(__name__)

HOST_IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

################################################################################
# Queries
################################################################################

QUERY_SHOW_DATABASES = """show databases;"""
QUERY_SHOW_TABLES = """show tables in {schema_name};"""
QUERY_TABLE_RECORDS_WITH_LIMIT = """select * from {schema_name}.{table_name} limit {limit};"""
QUERY_TABLE_RECORDS = """select * from {schema_name}.{table_name} limit 1000;"""

SERVICE_URL = f"http://{HOST_IP}:{PORT}"
# Athena services
API_GET_ATHENA_DATABASES = "/get_athena_databases"
API_GET_ATHENA_TABLES = "/get_athena_tables"
API_QUERY_ATHENA_TABLE = "/query_athena_table"
API_RUN_QUERY_ON_ATHENA = "/run_query_on_athena"
HEADERS = {
    'content-type': "application/json",
    'cache-control': "no-cache",
}


# TODO - Add user validation

################################################################################
# Athena Client
################################################################################

class AthenaClient:

    def __init__(self, user_name, password):
        self._user_name = user_name
        self._password = password

    def databases(self, result_as_df=True):
        """Returns all the schemas available in Athena"""
        try:
            payload = json.dumps({"user_name": self._user_name, "password": self._password})
            r = requests.post(SERVICE_URL + API_GET_ATHENA_DATABASES, data=payload, headers=HEADERS)
            response = r.json()
            if result_as_df:
                response_as_df = pd.DataFrame.from_dict(response)
                return response_as_df
            else:
                return response
        except requests.exceptions.HTTPError as err_h:
            # logger.error(msg=err_h)
            raise Exception("Http error occurred") from None
        except requests.exceptions.ConnectionError as err_c:
            # logger.error(msg=err_c)
            raise ConnectionError("Connection error occurred") from None
        except requests.exceptions.Timeout as err_t:
            # logger.error(msg=err_t)
            raise TimeoutError("Request timed out...") from None
        except requests.exceptions.RequestException as err:
            # logger.error(msg=err)
            raise Exception("RequestException occurred") from None

    def tables(self, schema_name, result_as_df=True):
        """Returns all the tables present in a schema"""
        try:
            payload = json.dumps({"user_name": self._user_name, "password": self._password, "schema_name": schema_name})
            r = requests.post(SERVICE_URL + API_GET_ATHENA_TABLES, data=payload, headers=HEADERS)
            response = r.json()
            if result_as_df:
                response_as_df = pd.DataFrame.from_dict(response)
                return response_as_df
            else:
                return response
        except requests.exceptions.HTTPError as err_h:
            # logger.error(msg=err_h)
            raise Exception("Http error occurred")
        except requests.exceptions.ConnectionError as err_c:
            # logger.error(msg=err_c)
            raise ConnectionError("Connection error occurred")
        except requests.exceptions.Timeout as err_t:
            # logger.error(msg=err_t)
            raise TimeoutError("Request timed out...")
        except requests.exceptions.RequestException as err:
            # logger.error(msg=err)
            raise Exception("RequestException occurred")

    def top(self, schema_name, table_name, limit=None, result_as_df=True):
        """Returns records from a table"""
        try:
            payload = json.dumps({"user_name": self._user_name, "password": self._password, "schema_name": schema_name,
                                  "table_name": table_name, "limit": limit})
            r = requests.post(SERVICE_URL + API_QUERY_ATHENA_TABLE, data=payload, headers=HEADERS)
            response = r.json()
            if result_as_df:
                response_as_df = pd.DataFrame.from_dict(response)
                return response_as_df
            else:
                return response
        except requests.exceptions.HTTPError as err_h:
            # logger.error(msg=err_h)
            raise Exception("Http error occurred")
        except requests.exceptions.ConnectionError as err_c:
            # logger.error(msg=err_c)
            raise ConnectionError("Connection error occurred")
        except requests.exceptions.Timeout as err_t:
            # logger.error(msg=err_t)
            raise TimeoutError("Request timed out...")
        except requests.exceptions.RequestException as err:
            # logger.error(msg=err)
            raise Exception("RequestException occurred")

    def run_query(self, query_string, result_as_df=True):
        """Run a specified query"""
        try:
            payload = json.dumps(
                {"user_name": self._user_name, "password": self._password, "query_string": query_string})
            r = requests.post(SERVICE_URL + API_RUN_QUERY_ON_ATHENA, data=payload, headers=HEADERS)
            response = r.json()
            if result_as_df:
                response_as_df = pd.DataFrame.from_dict(response)
                return response_as_df
            else:
                return response
        except requests.exceptions.HTTPError as err_h:
            # logger.error(msg=err_h)
            raise Exception("Http error occurred")
        except requests.exceptions.ConnectionError as err_c:
            # logger.error(msg=err_c)
            raise ConnectionError("Connection error occurred")
        except requests.exceptions.Timeout as err_t:
            # logger.error(msg=err_t)
            raise TimeoutError("Request timed out...")
        except requests.exceptions.RequestException as err:
            # logger.error(msg=err)
            raise Exception("RequestException occurred")
