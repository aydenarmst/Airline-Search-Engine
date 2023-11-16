from Ingestion.SparkIngestion import load_data
from pyspark.sql import SparkSession
from algos.Spark_Find_Airports_X_Country import find_airports_within_country


def main():
    spark = SparkSession.builder.appName("Airline Data Processing").getOrCreate()
    airport, airlines, routes = load_data(spark)
    choice = 0

    while choice != 7:
        print("1. Find Airports within a country")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            find_airports_within_country(airport, airlines, routes)
        elif choice == 7:
            break
        else:
            print("Invalid choice")
    
    spark.stop()

if __name__ == "__main__":
    main()
