from pyspark.sql.functions import col,lower, udf
import json
import time
from pyspark.sql.functions import lit
from queue import Queue
from pyspark.sql.types import IntegerType

from pyspark.sql.functions import collect_list

def queryDataframe(df, conditions):
    start_time = time.time()

    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())
    end_time = time.time()

    return result_df.toJSON().map(lambda j: json.loads(j)).collect(), end_time - start_time


def filterDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())

    return result_df


def findDHopsCities(airports_df, routes_df, hop_count,starting_airports):
    if hop_count < 1:
        print("Invalid Hop Count")
        return
    start_time = time.time()

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

    return intersecting_rows.select("City", "Level").toJSON().map(lambda j: json.loads(j)).collect(), end_time-start_time





def findTrip(routes_df, source_airport, destination_airport):
    # BFS
    visited = set()
    queue = Queue()
    start_time = time.time()
    queue.put((source_airport, []))  # (airport, path_to_airport)
    while not queue.empty():
        current_airport, path = queue.get()
        
        if current_airport == destination_airport:
            json_path = [row.asDict() for row in path]
            end_time = time.time()
            print(f"Spark found routes in: {end_time - start_time} seconds\n")
            return json_path

        if current_airport in visited:
            continue
        visited.add(current_airport)

        next_routes = routes_df.filter(col("Source airport") == current_airport)
        for row in next_routes.collect():
            dest_airport = row["Destination airport"]
            if dest_airport not in visited:
                new_path = path + [row]
                queue.put((dest_airport, new_path))


def find_trip(routes_df, source_airport, destination_airport):
    routes_dict = routes_df.groupBy("Source airport").agg(collect_list("Destination airport").alias("Destinations")).rdd.collectAsMap()

    # BFS
    visited = set()
    queue = Queue()
    start_time = time.time()
    queue.put((source_airport, []))  # (airport, path_to_airport)
    while not queue.empty():
        current_airport, path = queue.get()
        
        if current_airport == destination_airport:
            json_path = [row for row in path]
            end_time = time.time()
            print(f"Spark found routes in: {end_time - start_time} seconds\n")
            return json_path, end_time - start_time

        if current_airport in visited:
            continue
        visited.add(current_airport)

        next_routes = routes_dict.get(current_airport, [])
        for dest_airport in next_routes:
            if dest_airport not in visited:
                new_path = path + [dest_airport]
                queue.put((dest_airport, new_path))



def convertListToRoutes(routes_df, routes):
    # routeResults = []
    # for i in range(len(route) - 1):
    #     route = routes_df.filter((col("Source Airport") == route[i]) & (col("Destination Airport") == route[i+1])).first()
    #     routeResults.append(route)
    filter_conditions = [
    (col("Source airport") == routes[i]) & (col("Destination airport") == routes[i + 1])
    for i in range(len(routes) - 1)
    ]

    combined_condition = filter_conditions[0]
    for condition in filter_conditions[1:]:
        combined_condition = combined_condition | condition

    selected_routes_df = routes_df.filter(combined_condition)
    selected_routes_df = selected_routes_df.dropDuplicates(["Source airport", "Destination airport"])
    # l = []
    # for i in routes:
    #     l.append(selected_routes_df.filter(col("Source Airport") == i))
    # print(l)
    index_udf = udf(lambda x: routes.index(x), IntegerType())
    selected_routes_df = selected_routes_df.withColumn("index", index_udf(col("Source airport")))
    # selected_routes_df = selected_routes_df.orderBy(keyFunc=lambda x : routes.index(x["Source Airport"]))
    selected_routes_df = selected_routes_df.orderBy("index")
    selected_routes_df = selected_routes_df.drop("index")
    return selected_routes_df.toJSON().map(lambda j: json.loads(j)).collect()

def country_most_airports(airports_df):
    start_time = time.time()
    airports_in_country = (airports_df.groupBy(airports_df.schema.names[3]).count()).orderBy(col("count").desc())
    airports_in_country.limit(1).show()
    end_time = time.time()
    print(f"Spark algorithm took: {end_time - start_time} seconds\n")


def find_airports_within_country(airports_df, country):
    country = country.lower()
    start_time = time.time()
    airports_in_country = airports_df.filter(lower(airports_df["Country"]) == country)
    end_time = time.time()
    print(f"Airport count: {airports_in_country.count()}")
    print(f"Spark find airports within country took: {end_time - start_time} seconds\n")
    return airports_in_country.toJSON().map(lambda j: json.loads(j)).collect()