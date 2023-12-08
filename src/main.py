from pyspark.sql.functions import lower
from algos.Find_Airports_X_Country import find_airports_within_country
from algos.Spark_MostAirports import country_most_airports
from algos.Spark_Gabe import find_active_airlines_x_country
from algos.Spark_Queries import queryDataframe,findDHopsCities, filterDataframe
from Ingestion.SparkIngestion import load_data
from Connector.writeDF import write_to_Neo4j
from pyspark.sql import SparkSession
from neo4j import GraphDatabase

import http.server
import socketserver
import os
import json


#     # Neo4j credentials
# new_uri = "neo4j+s://cdc70305.databases.neo4j.io:7687"
# new_password = "2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI"
# username = "neo4j"

# sets the jar from maven repo for neo4j-connector-apache-spark
spark = (SparkSession.builder 
    .appName("Airline Data Processing") 
    .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.2.0_for_spark_3") 
    .getOrCreate())

# First load the data into spark dataframes for processing
use_reduced_data = True
airport, airlines, routes = load_data(spark, use_reduced_data)

# result = findDHopsCities(airport,routes,"Dallas-Fort Worth",2)
# print(result)

# Write the dataframes to AuraDB, commented out bc only need to write when performance testing
# write_to_Neo4j(airport, airlines, routes)

# Initialize the driver to connect to Neo4j AuraDB
# driver = GraphDatabase.driver(new_uri, auth=(username, new_password))
# exit(1)
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Data", post_data)
        post_data = json.loads(post_data)

        if self.path == '/data':
            response_data = self.handle_data_post(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def handle_data_post(self, data):
        result = {}
        if(data["function"] == "findAirline"):
            result = queryDataframe(df=airlines, conditions=json.loads(data["conditions"]))
        elif(data["function"] == "findAirports"):
            result = queryDataframe(df=airport, conditions=json.loads(data["conditions"]))
        elif(data["function"] == "findRoutes"):
            result = queryDataframe(df=routes, conditions=json.loads(data["conditions"]))
        elif(data["function"] == "findDHopsCities"):
            conditions = json.loads(data["conditions"])
            result = findDHopsCities(airports_df=airport, routes_df=routes, hop_count=int(data["Hop Count"]), starting_airports=filterDataframe(airport, conditions))
        return result

PORT = 8080

web_dir = "."
os.chdir(web_dir)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")

    # Start the server
    httpd.serve_forever()
    



    
# choice = 0
# while choice != 7:
#     print("1. Find Airports within a country")
#     print("2. Find country with most airports")
#     print("3. Find Active Airlines within a country")
#     print("4. Find all cities reachable within d hops")
#     print("7. Exit")
#     choice = int(input("Enter your choice: "))
    
#     if choice == 1:
#         find_airports_within_country(airport)
#     elif choice == 2:
#         country_most_airports(airport)
#     elif choice == 3:
#         find_active_airlines_x_country(airport, airlines, routes)
#     elif choice == 4:
#         find_all_cities_reachable_within_d_hops(airport,airlines,routes)
#     elif choice == 7:
#         break
#     else:
#         print("Invalid choice")

# spark.stop()


