from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import Table
import os
from dotenv import load_dotenv

load_dotenv()

source_engine = create_engine(f'mssql+pyodbc://'
                              f'{os.getenv("SOURCE_DB_USER")}'
                              f':{os.getenv("SOURCE_DB_PASSWORD")}'
                              f'@{os.getenv("SOURCE_DB_DSN")}',
                              echo=True)

metadata = MetaData(source_engine)
metadata.reflect(bind=source_engine)

view = Table('vReport_TimeDetail', metadata, autoload=True)
