""" conversion.acquirer.py pulls data and tracks what has been pulled from the source.db




"""

from dotenv import load_dotenv
import os
import logging
import pandas as pd
import time
from sqlalchemy import create_engine

from setup_logging import setup_logger

# setup logging
logger = logging.getLogger(__name__)
setup_logger(logger, 'logs/acquisition.log')

# load .env file for access by os
load_dotenv()


class DataSourceEngine:

    def __init__(self):
        self.engine = create_engine(f'mssql+pyodbc://'
                                    f'{os.getenv("SOURCE_DB_USER")}'
                                    f':{os.getenv("SOURCE_DB_PASSWORD")}'
                                    f'@{os.getenv("SOURCE_DB_DSN")}',
                                    echo=True)

    def __repr__(self):
        return f'{self.__class__.__name__} object'

    def __return_queried_list_of_table_names(self, table_type: str) -> list:
        """Queries a list of tables names from the Source DB.

        A Private method user be other methods to either return different table lists.

        Args:
            table_type (str): either 'BASE_TABLE' or 'VIEW'.

        Returns:
            List of strings representing table names.
        """
        try:
            # verify that the TABLE_TYPE passes is valid, if not raise ValueError
            acceptable_table_types = ['BASE_TABLE', 'VIEW']
            if table_type not in acceptable_table_types:
                raise ValueError(f'table_type must be in {acceptable_table_types}')

            # define the query based on the passed table_type
            query_string = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES " \
                           f"WHERE TABLE_TYPE = '{table_type}' AND TABLE_CATALOG = '{os.getenv('SOURCE_DB_CATALOG')}'"

            # query the table names and return a string
            df_table_names: pd.DataFrame = pd.read_sql(query_string, self.engine)
            logger.info(f"Queried '{table_type}' table types names. {len(df_table_names)} table names returned.")
            return sorted([x[0] for x in df_table_names.values.tolist()])

        # log exception if it happens
        except Exception as e:
            logging.error(e.args, exc_info=True)

    def return_table_name_list(self) -> list:
        """Queries and returns all table names WHERE TABLE_TYPE = 'BASE_TABLE' from the sources db.

        Returns:
            List of strings representing table names.
        """
        return self.__return_queried_list_of_table_names(table_type='BASE_VIEW')

    def return_view_name_list(self) -> list:
        """Queries and returns all table names WHERE TABLE_TYPE = 'VIEW' from the sources db.

        Returns:
            List of strings representing table names.
        """
        return self.__return_queried_list_of_table_names(table_type='VIEW')

    def query_column_names_and_types(self, table_name) -> pd.DataFrame:
        query_string = f"""
                SELECT 
                    c.name 'column_name',
                    t.Name 'data_type',
                    c.max_length 'max_length',
                    c.precision ,
                    c.scale ,
                    c.is_nullable,
                    ISNULL(i.is_primary_key, 0) 'primary_key'
                FROM    
                    sys.columns c
                INNER JOIN 
                    sys.types t ON c.user_type_id = t.user_type_id
                LEFT OUTER JOIN 
                    sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                LEFT OUTER JOIN 
                    sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
                WHERE
                    c.object_id = OBJECT_ID('{table_name}')
            """
        t1 = time.time()
        df = pd.read_sql(query_string, self.engine)
        t2 = time.time()
        df['table_name'] = table_name
        df['column_num'] = df.index + 1
        cols = df.columns.tolist()
        cols = cols[-2:] + cols[:7]
        df = df[cols]

        logger.info(f'Queried {table_name} column names and types. {round(t2 - t1, 4)} seconds')

        return df

    def save_all_table_info(self):

        views = self.return_view_name_list()

        for view in views:
            df = self.query_column_names_and_types(table_name=view)
            df.to_csv(f'docs/table_index/{view}.csv', index=False)

    def return_df_from_csv_info_file(self, path: str, table_name: str):

        df_info = pd.read_csv(path)
        columns = df_info['column_name'].tolist()

        df_table = pd.read_sql_table(table_name, self.engine, index_col=columns)

        return df_table
