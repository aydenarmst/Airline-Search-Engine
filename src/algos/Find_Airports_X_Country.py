import time
import json
from pyspark.sql.functions import lower
    
# Using Spark to find airports within a country
def find_airports_within_country(airports_df, country):
    country = country.lower()
    start_time = time.time()
    airports_in_country = airports_df.filter(lower(airports_df["Country"]) == country)
    end_time = time.time()
    # airports_in_country.show(airports_in_country.count(), False)
    print(f"Airport count: {airports_in_country.count()}")
    print(f"Spark find airports within country took: {end_time - start_time} seconds\n")
    return airports_in_country.toJSON().map(lambda j: json.loads(j)).collect()
    
    
# Neo4j version of finding airports within a country
# def find_airports_within_country(driver):
#     start_time = time.time()
#     country = input("Enter a country: ")
#     with driver.session() as session:
#         result = session.run(f"""MATCH (a:Airport)
#                                 WHERE a.Country = '{country}'
#                                 RETURN a""")
#         for record in result:
#             print(record[0]['Name'])
#         driver.close()
#     end_time = time.time()
#     print(f"Find airports within country took: {end_time - start_time} seconds")