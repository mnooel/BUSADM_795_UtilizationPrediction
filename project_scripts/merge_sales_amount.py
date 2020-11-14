from database_access import LiteDbConnection
from database_access import SourceDbConnection

# def merce_income_statement_account_types():
source = SourceDbConnection()
lite = LiteDbConnection()

df = source.query_df_from_sql_script('GL_Transactions.sql')

income_statement_account_types = ['Income', 'Cost of Goods Sold', 'Expense', 'Other Income', 'Other Expense']

for account_type in income_statement_account_types:
    new_label = account_type.replace(' ', '_')
    new_label = new_label.lower()
    mask = df.cond
    df[new_label] = 0.0
    df = df.loc[df[new_label] == new_label, new_label] = df['credit_amount'] - df['debit_amount']

df = df[df['account_type'] == 'Income']

df['income'] = df['credit_amount'] - df['debit_amount']

df = df[['date_posted', 'income']]
df.columns = ['date', 'income']

df_lite_date = lite.query_df_from_table_name('aTimeDate')

df_lite_date = df_lite_date.merge(df, how='outer', on=['date'])
df_lite_date['income'] = df_lite_date['income'].fillna(0)

lite.insert_df_as_table(df_lite_date, 'aTimeDate', index=False, if_exists='replace')

# if __name__ == '__main__':
#     merge_sales()
