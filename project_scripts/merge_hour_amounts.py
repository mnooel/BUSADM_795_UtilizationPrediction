# merge_hours_amounts.py

from database_access import LiteDbConnection
from database_access import SourceDbConnection


def merge_sales():
    source = SourceDbConnection()
    lite = LiteDbConnection()

    df = lite.query_df_from_table_name('tTime')


    df = df[df['account_type'] == 'Income']

    df['income'] = df['credit_amount'] - df['debit_amount']

    df = df[['date_posted', 'income']]
    df.columns = ['date', 'income']

    df_lite_date = lite.query_df_from_table_name('aTimeDate')

    df_lite_date = df_lite_date.merge(df, how='outer', on=['date'])
    df_lite_date['income'] = df_lite_date['income'].fillna(0)

    lite.insert_df_as_table(df_lite_date, 'aTimeDate', index=False, if_exists='replace')


if __name__ == '__main__':
    merge_sales()