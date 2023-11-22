import time

def find_airports_within_country(driver):
    start_time = time.time()
    country = input("Enter a country: ")
    with driver.session() as session:
        result = session.run(f"""MATCH (a:Airport)
                                WHERE a.Country = '{country}'
                                RETURN a""")
        for record in result:
            print(record[0]['Name'])
        driver.close()
    end_time = time.time()
    print(f"Find airports within country took: {end_time - start_time} seconds")
    
# NEXT: Define a trip as a sequence of connected route. Find a trip that connects two cities X and Y (reachability) 