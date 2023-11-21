from algos.Spark_Find_Airports_X_Country import find_airports_within_country
from Ingestion.SparkIngestion import load_data
from Connector.writeDF import write_to_auraDB
from pyspark.sql import SparkSession


def main():
    spark = (SparkSession.builder 
        .appName("Airline Data Processing") 
        .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.2.0_for_spark_3") 
        .getOrCreate())
    
    # First load the data into spark dataframes for processing
    airport, airlines, routes = load_data(spark)
    
    # Write the dataframes to AuraDB
    write_to_auraDB(airport, airlines, routes)

        
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
