# Write the dataframes to a neo4j database
# # Wait 60 seconds before connecting using these details, or login to https://console.neo4j.io to validate the Aura Instance is available
# NEO4J_URI=neo4j+s://cdc70305.databases.neo4j.io
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI
# AURA_INSTANCEID=cdc70305
# AURA_INSTANCENAME=Instance01

def write_to_auraDB(airports_df, airlines_df, routes_df):
    # SSL Handshake error when connecting to AuraDB w/o self-signed cert
    # Docs for this connection with the self-signed cert: https://aura.support.neo4j.com/hc/en-us/articles/4405119907859-Handling-SSL-errors-when-connecting-to-your-AuraDB-Instance
    neo4j_uri = "neo4j+ssc://cdc70305.databases.neo4j.io"
    neo4j_password="2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI"
    neo4j_username="neo4j"
    
    # Airline nodes
    (airlines_df.write.format("org.neo4j.spark.DataSource")
     .mode("Overwrite")
     .option("url", neo4j_uri)
     .option("authentication.type", "basic")
     .option("authentication.basic.username", neo4j_username)
     .option("authentication.basic.password", neo4j_password)
     .option("labels", "Airline")
     .option("node.keys", "Airline ID")
     .save())
    
    # airport nodes
    (airports_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("labels", "Airport")
        .option("node.keys", "Airport ID")
        .save())
    
    # route nodes
    (routes_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("labels", "Route")
        .option("node.keys", "RouteID")
        .save())
    
    relationship_query = """
                        MATCH (route:Route), (airport:Airport)
                        WHERE route.`Source airport ID`   = airport.`Airport ID`
                        MERGE (route)-[:DEPARTS_FROM]->(airport)
                        """
    (routes_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("batch.size", 200) # needed to avoid dbms memory issues
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("query", relationship_query)
        .save())
    
    # Relationship between route and airline
    relationship_query = """
                        MATCH (route:Route), (airport:Airport)
                        WHERE route.`Destination airport ID` = airport.`Airport ID`
                        MERGE (route)-[:ARRIVES_AT]->(airport)
                        """
                        
    (routes_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("batch.size", 200)
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("query", relationship_query)
        .save())  
    
        
    print("Data written to AuraDB")