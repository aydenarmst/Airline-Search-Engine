from neo4j import GraphDatabase
import json

def execute_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        return result


def find_active_US_airlines(driver):
    # stopcount = int(input("Enter Stop #: "))
    with driver.session() as session:
        result = session.run(f"""MATCH (a:Airline)
                                WHERE a.Active = 'Y' AND a.Country = 'United States'
                                RETURN a""")
        for record in result:
            print(record[0]['Name'])
        driver.close()

def find_cities_reachable_within_d_hops(driver):
    current_city = input("Enter a city: ")
    # current_city = "Dallas-Fort Worth"
    hop_count = int(input("Enter a hop count: "))
    hop_count = 2
    if(hop_count < 1):
        print("Hop count must be greater than 1")
        return
    cities = set()
    count = 1
    start = f"MATCH(a:`Source Airport`) WHERE a.City = '{current_city}'\n"
    middle = "MATCH (r0: Route {`Source airport` : a.IATA})-[g0]->(d0:`Destination Airport`)"
    end = "\nRETURN d0.City"
    while(count != hop_count):
        middle += f"\nMATCH (r{count}: Route {{`Source airport` : d{count-1}.IATA}})-[g{count}]->(d{count}:`Destination Airport`)\n"
        end += f",d{count}.City"
        count += 1
    with driver.session() as session:
        result = session.run(start+middle+end)
        for record in result:
            for r in record:
                cities.add(r)
        driver.close()
    print(cities)







uri = "neo4j+s://fc415e8e.databases.neo4j.io:7687"
username = "neo4j"
password = "suzSdYgWm9FkzztWHZXIExxv6kR9WoDzZeIVq8DgfOE"
driver = GraphDatabase.driver(uri, auth=(username, password))
# find_active_US_airlines(driver)
find_cities_reachable_within_d_hops(driver)

# with driver.session() as session:
#     result = session.run("MATCH(n:Airline) RETURN n")
#     for record in result:
#         print(record[0]['Airline ID'])

    # driver.close()