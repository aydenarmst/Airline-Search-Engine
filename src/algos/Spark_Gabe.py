import time
from pyspark.sql.functions import lit
def find_active_airlines_x_country(airports_df, airlines_df, routes_df):
    country = input("Enter the country name: ")
    start_time = time.time()
    active_airlines_in_country = airlines_df.filter((airlines_df.Country == country)& (airlines_df.Active == 'Y'))
    end_time = time.time()
    active_airlines_in_country.show(active_airlines_in_country.count(), False)
    print(f"Airport count: {active_airlines_in_country.count()}")
    print(f"Spark find active airlines in country took: {end_time - start_time} seconds\n")



def find_all_cities_reachable_within_d_hops(airports_df, airlines_df, routes_df):
    city = input("Enter the City name: ")
    # city = "Dallas-Fort Worth"
    hop_count = int(input("Enter a hop count: "))
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

    intersecting_rows = visited_airports.join(airports_df, "Airport ID", "inner").select("City")
    intersecting_rows.show()
    end_time = time.time()
    print(f"Spark find airlines in {hop_count} hops in: {end_time - start_time} seconds\n")
