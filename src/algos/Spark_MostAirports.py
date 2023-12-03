import time
from pyspark.sql.functions import col

def country_most_airports(airports_df):
    start_time = time.time()
    airports_in_country = (airports_df.groupBy(airports_df.schema.names[3]).count()).orderBy(col("count").desc())
    airports_in_country.limit(1).show()
    end_time = time.time()
    print(f"Spark algorithm took: {end_time - start_time} seconds\n")