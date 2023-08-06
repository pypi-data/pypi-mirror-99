#!/usr/bin/env python
import json
import logging
import requests
import socket
import pandas as pd

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

    def databases(self):
        """Returns all the schemas available in Athena"""
        try:
            payload = {"user_name": self._user_name, "password": self._password}
            # payload = "{\n\t\"user_name\":\"Karthik\",\n\t\"password\":\"1\"}"
            r = requests.post(SERVICE_URL + API_GET_ATHENA_DATABASES, data=json.dumps(payload), headers=HEADERS)
            response = r.json()
            return response
        except requests.exceptions.HTTPError as err_h:
            print(err_h)
        except requests.exceptions.ConnectionError as err_c:
            print(err_c)
        except requests.exceptions.Timeout as err_t:
            print(err_t)
        except requests.exceptions.RequestException as err:
            print(err)

    def tables(self, schema_name):
        """Returns all the tables present in a schema"""
        try:
            pay_load = {"user_name": self._user_name, "password": self._password, "schema_name": schema_name}
            r = requests.post(SERVICE_URL + API_GET_ATHENA_TABLES, data=pay_load, headers=HEADERS)
            response = r.json()
            return response
        except requests.exceptions.HTTPError as err_h:
            print(err_h)
        except requests.exceptions.ConnectionError as err_c:
            print(err_c)
        except requests.exceptions.Timeout as err_t:
            print(err_t)
        except requests.exceptions.RequestException as err:
            print(err)

    def top(self, schema_name, table_name, limit=None):
        """Returns records from a table"""
        try:
            pay_load = {"user_name": self._user_name, "password": self._password, "schema_name": schema_name,
                        "table_name": table_name, "limit": limit}
            r = requests.post(SERVICE_URL + API_QUERY_ATHENA_TABLE, data=pay_load, headers=HEADERS)
            response = r.json()
            return response
        except requests.exceptions.HTTPError as err_h:
            print(err_h)
        except requests.exceptions.ConnectionError as err_c:
            print(err_c)
        except requests.exceptions.Timeout as err_t:
            print(err_t)
        except requests.exceptions.RequestException as err:
            print(err)

    def run_query(self, query_string, result_as_df=True):
        """Run a specified query"""
        try:
            pay_load = {"user_name": self._user_name, "password": self._password, "query_string": query_string,
                        "result_as_df": result_as_df}
            r = requests.post(SERVICE_URL + API_RUN_QUERY_ON_ATHENA, data=pay_load, headers=HEADERS)
            response = r.json()
            if result_as_df:
                response_as_df = pd.DataFrame.from_dict(response, orient="index")
                return response_as_df
            else:
                return response
        except requests.exceptions.HTTPError as err_h:
            print(err_h)
        except requests.exceptions.ConnectionError as err_c:
            print(err_c)
        except requests.exceptions.Timeout as err_t:
            print(err_t)
        except requests.exceptions.RequestException as err:
            print(err)
