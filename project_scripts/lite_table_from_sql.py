# project_scripts.lite_table_from_sql.py

import logging

from database_access import SourceDbConnection
from database_access import LiteDbConnection
from setup_logging import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger, 'project_scripts.log')


def lite_table_from_sql(sql_file_name: str, table_name: str):

    try:
        # query data
        source = SourceDbConnection()
        df = source.query_df_from_sql_script(script_file_name=sql_file_name)

        # insert data
        lite = LiteDbConnection()
        lite.insert_df_as_table(df, table_name=table_name)
        logger.info(f'{table_name} created via {sql_file_name}. {len(df)} records created.')
    except Exception as e:
        logger.error(e.args)


if __name__ == '__main__':
    lite_table_from_sql('tProject.sql', 'tProject')
