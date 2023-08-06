#!/usr/bin/env python
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor


################################################################################
# Athena Utility
################################################################################

class PyAthenaLoader:

    def __init__(self):
        self.conn = None

    def connect(self, s3_staging_dir, region_name, schema_name=None, access_key_id=None,
                secret_access_key_id=None, botocore_session=None, aws_session_token=None):
        """Creates a connection to Athena"""
        try:
            conn = connect(
                s3_staging_dir=s3_staging_dir,
                region_name=region_name,
                schema_name=schema_name,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key_id,
                botocore_session=botocore_session,
                aws_session_token=aws_session_token,
                # cursor_class=PandasCursor,
            )
            if hasattr(self, 'conn'):
                self.conn.close()
            self.conn = conn
        except Exception as X:
            return X

    def databases(self):
        """Returns all the schemas available in Athena"""
        dbs = self.query("show databases;")
        return dbs

    def tables(self, database):
        """Returns all the tables present in a schema"""
        tables = self.query("show tables in {0};".format(database))
        return tables

    # def query(self, sql, parameters=None):
    #     """Execute query using cursor and parameters, and return the results as a Dataframe"""
    #     try:
    #         with self.conn.cursor() as athena_cursor:
    #             athena_cursor.execute(sql, parameters)
    #             result = athena_cursor.fetchall()
    #     except Exception as X:
    #         return X
    #     finally:
    #         self.conn.close()
    #     return result

    def query(self, sql, parameters=None):
        """Execute query using cursor and parameters, and returns the results as a dict"""
        try:
            with self.conn.cursor() as athena_cursor:
                athena_cursor.execute(sql, parameters)
                columns = [desc[0] for desc in athena_cursor.description]
                while True:
                    row = athena_cursor.fetchone()
                    if row is None:
                        break
                    yield dict(zip(columns, row))
        except Exception as X:
            return X
        finally:
            self.conn.close()


