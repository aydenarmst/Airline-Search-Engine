from algos.Find_Airports_X_Country import find_airports_within_country
from algos.Spark_MostAirports import country_most_airports
from Ingestion.SparkIngestion import load_data
from Connector.writeDF import write_to_Neo4j
from pyspark.sql import SparkSession
from neo4j import GraphDatabase


def main():
    # Neo4j credentials
    new_uri = "neo4j+s://cdc70305.databases.neo4j.io:7687"
    new_password = "2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI"
    username = "neo4j"
    
    # sets the jar from maven repo for neo4j-connector-apache-spark
    spark = (SparkSession.builder 
        .appName("Airline Data Processing") 
        .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.2.0_for_spark_3") 
        .getOrCreate())
    
    # First load the data into spark dataframes for processing
    use_reduced_data = True
    airport, airlines, routes = load_data(spark, use_reduced_data)
    

    # Write the dataframes to AuraDB, commented out bc only need to write when performance testing
    # write_to_Neo4j(airport, airlines, routes)
    
    # Initialize the driver to connect to Neo4j AuraDB
    driver = GraphDatabase.driver(new_uri, auth=(username, new_password))

        
    choice = 0
    while choice != 7:
        print("1. Find Airports within a country")
        print("2. Find country with most airports")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            find_airports_within_country(airport)
        elif choice == 2:
            country_most_airports(airport)
        elif choice == 7:
            break
        else:
            print("Invalid choice")
    
    spark.stop()

if __name__ == "__main__":
    main()
