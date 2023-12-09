from pyspark.sql.functions import col,lower
import json
import time
from pyspark.sql.functions import lit
from queue import Queue

def queryDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())

    return result_df.toJSON().map(lambda j: json.loads(j)).collect()


def filterDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())

    return result_df

def findDHopsCities(airports_df, routes_df, hop_count,starting_airports):
    # city = input("Enter the City name: ")
    # city = "Dallas-Fort Worth"
    # hop_count = int(input("Enter a hop count: "))
    # hop_count = 2

    if hop_count < 1:
        print("Invalid Hop Count")
        return
    start_time = time.time()
    # starting_airports = airports_df.filter(airports_df.City == city).select("Airport ID", "City")
    starting_airports = starting_airports.select("Airport ID", "City")
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
    end_time = time.time()
    print(f"Spark find airlines in {hop_count} hops in: {end_time - start_time} seconds\n")

    return intersecting_rows.select("City", "Level").toJSON().map(lambda j: json.loads(j)).collect()





def findTrip(routes_df, source_airport, destination_airport):
    # BFS dawg
    visited = set()
    queue = Queue()
    print("start")
    start_time = time.time()
    source_airport = source_airport.strip().upper()
    destination_airport = destination_airport.strip().upper()

    queue.put((source_airport, []))  # (airport, path_to_airport)
    while not queue.empty():
        current_airport, path = queue.get()
        
        if current_airport == destination_airport:
            json_path = [row.asDict() for row in path]

            end_time = time.time()
            print(f"Spark found routes in: {end_time - start_time} seconds\n")
            return json.dumps(json_path)

        if current_airport in visited:
            continue
        visited.add(current_airport)

        next_routes = routes_df.filter(col("Source airport") == current_airport)
        for row in next_routes.collect():
            dest_airport = row["Destination airport"]
            if dest_airport not in visited:
                new_path = path + [row]
                queue.put((dest_airport, new_path))
