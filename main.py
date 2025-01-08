import duckdb
import pandas as pd

conn = duckdb.connect("data/retail_sales.duckdb")
# df = conn.sql("SELECT * FROM sales").df()
# print(df)
# # after preprocessing via dbt is done, you can retrieve the target data for example in the following manner.

# tables = conn.execute("SHOW TABLES").fetchall()
# print(tables)

# #Query with ORDER BY to ensure consistent row ordering
# df_target_series = conn.sql("""
#     SELECT * 
#     FROM dbt.target_time_series
#     ORDER BY item_id, date
# """).df()

# #Print the first 10 rows
# print(df_target_series.head(30), len(df_target_series))

# # #Query with ORDER BY to ensure consistent row ordering
# df_meta_data = conn.sql("""
#     SELECT * 
#     FROM dbt.meta_data
#     ORDER BY date, item_name
#     LIMIT 10000
# """).df()
# df_meta_data = df_meta_data.fillna(0)
# print(df_meta_data.tail(100))


# # Query with ORDER BY to ensure consistent row ordering
# df_per_item_cov = conn.sql("""
#     SELECT * 
#     FROM dbt.per_item_covariates
#     ORDER BY item_id, date
#     LIMIT 1000
# """).df()

# print(df_per_item_cov.head(30), len(df_per_item_cov))

# # Query with ORDER BY to ensure consistent row ordering
# df_meta_data = conn.sql("""
#     SELECT * 
#     FROM dbt.data_for_forecasting
#     ORDER BY date
#     LIMIT 1000
# """).df()
# df_meta_data = df_meta_data.fillna(0)
# print(len(df_meta_data), df_meta_data.tail(50))
