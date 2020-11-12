# settings.py

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = PROJECT_DIR + '/logs'
TABLE_INFO_DIR = PROJECT_DIR + '/docs/table_info'
CSV_TABLE_DIR = PROJECT_DIR + '/docs/csv_table_data'
LITE_DB_PATH = PROJECT_DIR + '/data.sqlite'
LITE_DB_URL = 'sqlite:///' + LITE_DB_PATH
SOURCE_DB_URL = f'mssql+pyodbc://' \
                f'{os.getenv("SOURCE_DB_USER")}' \
                f':{os.getenv("SOURCE_DB_PASSWORD")}' \
                f'@{os.getenv("SOURCE_DB_DSN")}'
SQL_SCRIPT_DIR = PROJECT_DIR + '/SQL'
SOURCE_SQL_SCRIPT_DIR = SQL_SCRIPT_DIR + '/source_db'
LITE_SQL_SCRIPT_DIR = SQL_SCRIPT_DIR + '/lite_db'
