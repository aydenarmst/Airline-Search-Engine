import time
import json
import sys
from pyspark.sql.functions import col,lower, udf

def reduceWrapper(airport, routes,hop_count, starting_airports):
    tuple_starting = starting_airports.rdd.map(lambda row: (row['Airport ID'], row['City']))
    tuple_airports = airport.rdd.map(lambda row: (row['Airport ID'], row['City']))
    tuple_routes = routes.rdd.map(lambda row: (row['Source airport ID'], row['Destination airport ID'], row['Destination airport']))

    hops,time = reduceDHopsCities(tuple_airports, tuple_routes, hop_count, tuple_starting)
    result = {}
    for x in hops:
        result[x[1][1]] = min(x[1][0], result.get(x[1][1],sys.maxsize))
    result = [{"City" : k, "Level" :v} for k, v in sorted(result.items(), key=lambda item: item[1])]
    return result, time

def reduceDHopsCities(airports_rdd, routes_rdd, hop_count, starting_airports):
    if hop_count < 1:
        print("Invalid Hop Count")
        return
    start_time = time.time()

    current_level = starting_airports.map(lambda row: (row[0], 0))

    for i in range(1, hop_count + 1):
        next_level = current_level.join(routes_rdd).map(lambda row: (row[1][1], i))
        current_level = current_level.union(next_level).distinct()

    intersecting_rows = current_level.join(airports_rdd).distinct()
    intersecting_rows = sorted(intersecting_rows.collect(), key= lambda x:x[1][1])
    end_time = time.time()
    print(f"Spark find airlines in {hop_count} hops in: {end_time - start_time} seconds\n")

    # return intersecting_rows, end_time-start_time
    return intersecting_rows, end_time-start_time

def pathWrapper(routes, source_airport, dest_airport):
    tuple_routes = routes.rdd.map(lambda row: (row['Source airport ID'], row['Destination airport ID'], row['Destination airport']))
    

