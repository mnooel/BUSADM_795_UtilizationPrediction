# database_access.connections.py

import logging
import time
from typing import List

from sqlalchemy import create_engine
from sqlalchemy import MetaData
import pandas as pd

from settings import SOURCE_DB_URL
from settings import LITE_DB_URL
from settings import SOURCE_SQL_SCRIPT_DIR
from settings import LITE_SQL_SCRIPT_DIR
from setup_logging import setup_logger

connections_logger = logging.getLogger(__name__)
setup_logger(connections_logger, 'connections.log')


class BaseConnection:

    def __init__(self, db_url: str, write_permission: bool, sql_scrip_dir: str):
        self.engine = create_engine(db_url, echo=True)
        self.write_permission = write_permission
        self.sql_script_dir = sql_scrip_dir
        self.metadata: MetaData = None

    def __repr__(self):
        return f'{__class__.__name__}'

    def query_metadata(self):
        try:
            t1 = time.time()
            self.metadata = MetaData(self.engine)
            self.metadata.reflect(bind=self.engine)
            t2 = time.time()
            diff = round(t2 - t1, 4)
            connections_logger.info(f'{self.__repr__()} queried. Exe seconds: {diff}.')
        except Exception as e:
            connections_logger.error(e.args)

    def read_sql_commands_from_script(self, script_file_name: str) -> List[str]:
        """Reads .sql and returns a list of all the commands contained."""
        try:
            script_file_path = self.sql_script_dir + '/' + script_file_name
            print(script_file_path)
            with open(script_file_path, 'r') as file:
                sql_script = file.read()
                file.close()
            sql_commands = sql_script.split(';')
            return sql_commands[:-1]  # remove the last one because it just an empty string always.

        except Exception as e:
            connections_logger.error(e.args)

    def query_df_from_sql_script(self, script_file_name: str, **pd_kwargs) -> pd.DataFrame:
        try:
            sql_commands = self.read_sql_commands_from_script(script_file_name)
            if len(sql_commands) > 1:
                raise ValueError(f'{script_file_name} for {self.__repr__()} has more than one command. '
                                 f'This is not advisable.')
            else:
                t1 = time.time()
                df = pd.read_sql(sql_commands[0], self.engine, **pd_kwargs)
                t2 = time.time()
                diff = round(t2 - t1, 4)
                connections_logger.info(f'{self.__repr__()} {script_file_name} queried. Exe seconds: {diff}.')
                return df

        except Exception as e:
            connections_logger.error(e.args)

    def insert_df_as_table(self, df: pd.DataFrame, table_name: str, **pd_kwargs) -> None:
        try:
            if self.write_permission is False:
                raise PermissionError(f'{self.__repr__()}.write_permission = False.',
                                      'Inserting data to db is prohibited.')
            else:
                print(type(pd_kwargs))
                df.to_sql(table_name, self.engine, **pd_kwargs)

        except Exception as e:
            connections_logger.error(e.args)


class SourceDbConnection(BaseConnection):

    def __init__(self):
        super(SourceDbConnection, self).__init__(db_url=SOURCE_DB_URL,
                                                 write_permission=False,
                                                 sql_scrip_dir=SOURCE_SQL_SCRIPT_DIR)

    def __repr__(self):
        return f'{__class__.__name__}'


class LiteDbConnection(BaseConnection):

    def __init__(self):
        super(LiteDbConnection, self).__init__(db_url=LITE_DB_URL,
                                               write_permission=True,
                                               sql_scrip_dir=LITE_SQL_SCRIPT_DIR)

    def __repr__(self):
        return f'{__class__.__name__}'
