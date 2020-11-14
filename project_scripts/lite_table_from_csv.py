# project_scripts.lite_table_from_csv.py

import logging

import pandas as pd

from database_access import LiteDbConnection
from setup_logging import setup_logger
from settings import CSV_TABLE_DIR

logger = logging.getLogger(__name__)
setup_logger(logger, 'project_scripts.log')


def main(csv_file_name: str):

    path = CSV_TABLE_DIR + '/' + csv_file_name
    df = pd.read_csv(path)
    lite = LiteDbConnection()

    lite.insert_df_as_table(table_name=csv_file_name[:-4], df=df, chunksize=10000)
    logger.info(f'Ran {__name__} successfully.')


if __name__ == '__main__':
    main('vReport_TimeDetail_v1.csv')
