from pyspark.sql import SparkSession
from Ingestion.SparkSchema import SparkSchema
from Ingestion.DataConfig import DataConfig


def load_data():
    # Init spark session
    spark = SparkSession \
            .builder \
            .appName("Airline Data Processing") \
            .getOrCreate()

    # read the csv files into dataframes
    airports_df = spark.read.csv(
        DataConfig.get_path("airports"),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.airport_schema
    )

    airlines_df = spark.read.csv(
        DataConfig.get_path("airlines"),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.airline_schema
    )

    routes_df = spark.read.csv(
        DataConfig.get_path("routes"),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.route_schema
    )
    return airports_df, airlines_df, routes_df

