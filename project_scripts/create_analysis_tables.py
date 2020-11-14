# project_scripts.create_analysis_tables.py

import pandas as pd
from datetime import datetime
from database_access import LiteDbConnection


def create_analysis_tables():
    lite = LiteDbConnection()

    # create a list of dates
    start = datetime(2013, 1, 1)
    end = datetime(2020, 10, 31)
    dates_series = pd.date_range(start=start, end=end)

    df = pd.DataFrame(dates_series, columns=['date'])

    df['month_int'] = df.date.dt.month
    df['year_int'] = df.date.dt.year
    df['period_str'] = df['month_int'].map("{:02}".format) + pd.Series(['-'] * len(df)) + df['year_int'].astype(str)

    lite.insert_df_as_table(df=df, table_name='aTimeDate', if_exists='replace', index=False)

    df_grouped = df.groupby(['month_int', 'year_int', 'period_str'], as_index=False, sort=False)[['date']].count()
    df_grouped.rename(columns={'date':'number_of_days'}, inplace=True)

    lite.insert_df_as_table(df_grouped, 'aTimeMonth', if_exists='replace', index=False)


if __name__ == '__main__':
    create_analysis_tables()
