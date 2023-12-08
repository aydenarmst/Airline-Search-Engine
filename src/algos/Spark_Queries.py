from pyspark.sql.functions import col
import json
import time
from pyspark.sql.functions import lit

def queryDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(col(key) == value)

    return result_df.toJSON().map(lambda j: json.loads(j)).collect()

def findDHopsCities(airports_df, routes_df, city, hop_count):
    # city = input("Enter the City name: ")
    # city = "Dallas-Fort Worth"
    # hop_count = int(input("Enter a hop count: "))
    # hop_count = 2

    if hop_count < 1:
        print("Invalid Hop Count")
        return
    start_time = time.time()
    starting_airports = airports_df.filter(airports_df.City == city).select("Airport ID", "City")
    current_level = starting_airports.withColumn("Level", lit(0))

    visited_airports = current_level.select("Airport ID")

    for i in range(1, hop_count + 1):
        next_level = current_level.join(routes_df, current_level["Airport ID"] == routes_df["Source airport ID"]) \
            .select("Destination airport ID", "Destination airport", "Level") \
            .withColumnRenamed("Destination airport ID", "Airport ID") \
            .withColumnRenamed("Destination airport", "City") \
            .withColumn("Level", lit(i))

        next_level = next_level.join(visited_airports, "Airport ID", "leftanti")

        current_level = current_level.union(next_level)

        visited_airports = visited_airports.union(next_level.select("Airport ID"))
    
    intersecting_rows = current_level.select("Airport ID", "Level").join(airports_df, "Airport ID", "left_outer")
    # intersecting_rows = visited_airports.join(current_level, "Airport ID", "inner").select("City","Level")
    # intersecting_rows.show(5)
    # airports_df.show(5)
    # visited_airports.show(5)
    end_time = time.time()
    print(f"Spark find airlines in {hop_count} hops in: {end_time - start_time} seconds\n")

    return intersecting_rows.select("City", "Level").toJSON().map(lambda j: json.loads(j)).collect()
