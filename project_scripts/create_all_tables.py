# project_scripts.create_all_tables.py

import logging
import timeit
import pandas as pd

from database_access import SourceDbConnection
from database_access import LiteDbConnection


def create_all_tables():

    source = SourceDbConnection()
    lite = LiteDbConnection()

    # get metadata of the source table
    source.query_metadata()

    # list of table names
    table_names = [table for table in source.metadata.tables]

    # iterate over table names
    for table in table_names:
        if table[0] == 't':
            df = source.query_df_from_table_name(table)
            if isinstance(df, pd.DataFrame):
                lite.insert_df_as_table(df, table)
            else:
                pass


if __name__ == '__main__':
    import logging
    from setup_logging import setup_logger
    script_logger = logging.getLogger('create_all_tables.py')
    import time
    setup_logger(script_logger, 'scripts.log')

    try:
        t1 = time.time()
        create_all_tables()
        t2 = time.time()
        diff = round(t2 - t1, 4)
        script_logger.info(f'success. Seconds: {diff}')
    except Exception as e:
        script_logger.error(e.args)
