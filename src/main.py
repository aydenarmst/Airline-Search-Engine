from Ingestion.SparkIngestion import load_data
from pyspark.sql import SparkSession
from algos.Spark_Find_Airports_X_Country import find_airports_within_country
from Connector.writeDF import write_to_auraDB
# # Wait 60 seconds before connecting using these details, or login to https://console.neo4j.io to validate the Aura Instance is available
# NEO4J_URI=neo4j+s://cdc70305.databases.neo4j.io
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI
# AURA_INSTANCEID=cdc70305
# AURA_INSTANCENAME=Instance01
from pyspark.sql.functions import col, when, count




def main():
    spark = (SparkSession.builder 
        .appName("Airline Data Processing") 
        .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.2.0_for_spark_3") 
        .getOrCreate())
    
    
    airport, airlines, routes = load_data(spark)
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
