import logging
import os
import pandas as pd
from typing import Optional

import pandas as pd
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection

from pyrasgo.monitoring import track_usage
from pyrasgo.storage.base import DataWarehouse, DataWarehouseSession
from pyrasgo.session import Session
from pyrasgo.utils import dataframe


class SnowflakeDataWarehouse(DataWarehouse, Session, metaclass=DataWarehouseSession):
    def __init__(self):
        username = self.profile.get("snowUsername", None)
        if username is None:
            raise EnvironmentError("Your user is missing credentials, please contact Rasgo support.")
        self.username = username

        organization = self.profile.get("organization")
        self.org_prefix = organization.get("rolePrefix", "code")
        if self.org_prefix is None:
            raise EnvironmentError("Your organization is missing credentials, please contact Rasgo support.")

        self.password = self.profile.get("snowPassword")
        self.account = organization.get("account")
        self.database = organization.get("database")
        self.schema = organization.get("schema")
        self.warehouse = organization.get("warehouse")
        self.user_role = self.profile.get("snowRole", f"{self.org_prefix}_{self.username}")

    @property
    def rasgo_admin_role(self):
        return "RASGOADMIN"

    @property
    def admin_role(self):
        return f"{self.org_prefix}ADMIN"

    @property
    def publisher_role(self):
        return f"{self.org_prefix}PUBLISHER"

    @property
    def reader_role(self):
        return f"{self.org_prefix}READER"

    @property
    def public_role(self):
        return "PUBLIC"

    @property
    @track_usage
    def user_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.user_credentials)

    @property
    @track_usage
    def user_credentials(self) -> dict:
        return {
            "user": self.username,
            "password": self.password,
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.user_role
        }

    @property
    @track_usage
    def admin_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.admin_credentials)

    @property
    @track_usage
    def admin_credentials(self) -> dict:
        # TODO: This is an intentionally half-baked implementation to be completed when the need is clearer
        # 1) Most users won't have access to the admin role, so this will return an access error
        #    At some point we may want to pass in the org service account info to assume the admin role 
        # 2) The <org>admin role still has limited privileges and may fail on most 'admin' operations
        #    At some point we may want to run this as rasgoadmin if there are enough legitimate use cases that need it 
        return {
            "user": self.username, # SA user here
            "password": self.password, # SA pw here
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.admin_role #or RasgoAdmin?
        }

    @track_usage
    def execute_query(self, query: str, params: Optional[dict] = None, as_admin: Optional[bool] = False):
        """
        Execute a query on the [cloud] data platform.

        :param query: String to be executed on the data platform
        :param params: Optional parameters
        :param as_admin: Flag on whether to run the query as the admin role.
        :return:
        """
        if as_admin:
            return self.admin_connection.cursor().execute(query, params)
        return self.user_connection.cursor().execute(query, params)

    @track_usage
    def query_into_dataframe(self, query: str, params: Optional[dict] = None, 
                                   as_admin: Optional[bool] = False) -> pd.DataFrame:
        """
        Execute a query on the [cloud] data platform.

        :param query: String to be executed on the data platform
        :param params: Optional parameters
        :param as_admin: Flag on whether to run the query as the admin role.
        :return:
        """
        cur = self.admin_connection.cursor() if as_admin else self.user_connection.cursor()
        cur.execute(query, params)
        return cur.fetch_pandas_all()

    @track_usage
    def get_source_table(self, table_name: str, database: Optional[str] = None, schema: Optional[str] = None,
                         record_limit: Optional[int] = None) -> pd.DataFrame:
        if record_limit is None:
            logging.info(f"Loading all rows from {table_name}...")
        database = database or self.database
        schema = schema or self.schema
        result_set = self.execute_query(f"SELECT * FROM {database}.{schema}.{table_name} {f'LIMIT {record_limit}' if record_limit else ''}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_tables(self, database: Optional[str] = None, schema: Optional[str] = None):
        database = database or self.database
        schema = schema or self.schema
        filters = f"WHERE TABLE_SCHEMA='{schema}'"
        result_set = self.execute_query(f"SELECT TABLE_NAME, TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME AS FQTN, ROW_COUNT, TABLE_OWNER, CREATED, LAST_ALTERED FROM {database}.INFORMATION_SCHEMA.TABLES {filters}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None):
        database = database or self.database
        schema = schema or self.schema
        filters = f"WHERE TABLE_SCHEMA='{schema}'"
        filters += f" AND TABLE_NAME='{table}'" if table else ""
        filters += f" AND DATA_TYPE='{data_type}'" if data_type else ""
        result_set = self.execute_query(f"SELECT COLUMN_NAME, DATA_TYPE, TABLE_NAME, TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME AS FQTN FROM {database}.INFORMATION_SCHEMA.COLUMNS {filters}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def grant_table_ownership(self, table: str, role: str, database: Optional[str] = None, schema: Optional[str] = None):
        """
        Grants ownership of a table or FQTN to specified role
        Note: If user role is not the table owner, this will fail
        """
        database = database or self.database
        schema = schema or self.schema
        self.execute_query(f"GRANT OWNERSHIP ON {database}.{schema}.{table} TO ROLE {role} REVOKE CURRENT GRANTS;")
    
    @track_usage
    def grant_table_access(self, table: str, role: str, database: Optional[str] = None, schema: Optional[str] = None):
        """
        Grants select privilege on a table or FQTN to specified role
        Note: If user role does not have access with grant option, this will fail
        """
        database = database or self.database
        schema = schema or self.schema
        self.execute_query(f"GRANT SELECT ON {database}.{schema}.{table} TO ROLE {role};")

    @track_usage
    def clone_table(self, existing_table: str, new_table: str, overwrite: bool = False):
        """
        Clones a table or FQTN
        Note: if user role doesn't have select & create access to db + schema + table this will fail
        """
        if overwrite:
            self.execute_query(f"CREATE OR REPLACE TABLE {new_table} CLONE {existing_table};")
        else:
            self.execute_query(f"CREATE TABLE {new_table} CLONE {existing_table};")

    @track_usage
    def append_to_table(self, from_table: str, into_table: str):
        """
        Inserts data from a table or FTQN into another table or FQTN
        Note: if user role doesn't have select & modify access to db + schema + table this will fail
        """
        self.execute_query(f"INSERT INTO {into_table} SELECT * FROM {from_table};")

    def _make_table_metadata(self, table: str):
        if table.count(".") > 0:
            table = table.split(".")[-1]
        metadata = {
            "database": self.database,
            "schema": self.schema,
            "table": table,
        }
        return metadata

    def _write_dataframe_to_table(self, df: pd.DataFrame, table_name: str, append: Optional[bool] = False):
        """
        Note: we will allow users to select from other database, but only to write into org default database
        """
        from snowflake.connector.pandas_tools import write_pandas

        self._snowflakify_dataframe(df)
        write_pandas(conn=self.user_connection, df=df, table_name=self._snowflakify_name(table_name), quote_identifiers=False)

    @classmethod
    def _snowflakify_data_type(cls, dtype: str):
        if dtype.lower() in ["object", "text"]:
            return "string"
        else:
            return dtype.lower()

    @classmethod
    def _snowflakify_dataframe(cls, df: pd.DataFrame):
        """
        Renames all columns in a pandas dataframe to Snowflake compliant names in place
        """
        df.rename(columns={r: cls._snowflakify_name(r) for r in dataframe.build_schema(df)},
                  inplace=True)

    @classmethod
    def _snowflakify_list(cls, list_in):
        """
        param list_in: list
        return list_out: list
        Changes a list of columns to Snowflake compliant names
        """
        return [cls._snowflakify_name(n) for n in list_in]

    @staticmethod
    def _snowflakify_name(name):
        """
        param name: string
        return: string
        Converts a string to a snowflake compliant value
        Removes double quotes, replaces dashes/dots/spaces with underscores, casts to upper case
        """
        return name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".","_").upper()
