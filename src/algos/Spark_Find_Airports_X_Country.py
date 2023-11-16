import time


def find_airports_within_country(airports_df, airlines_df, routes_df):
    country = (input("Enter the country name: "))

    start_time = time.time()
    airports_in_country = airports_df.filter(airports_df.Country == country)
    end_time = time.time()
    airports_in_country.show(airports_in_country.count(), False)
    print(f"Airport count: {airports_in_country.count()}")
    print(f"Spark find airports within country took: {end_time - start_time} seconds\n")
