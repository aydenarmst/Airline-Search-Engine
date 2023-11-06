from neo4j import GraphDatabase
import json

def execute_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        return result


def find_active_US_airlines():
    f = open('reducedAirlines.csv', 'r')
    for airline in f:
        parameters = airline.strip().split(",")
        if(parameters[6] == "United States" and parameters[7] == 'Y'):
            print(parameters[1])

def find_cities_reachable_within_d_hops(driver):
    current_city = input("Enter a city: ")
    hop_count = int(input("Enter a hop count: "))
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
    if(len(cities) == 0):
        print("No hops found")
    else:
        print(cities)







uri = "neo4j+s://fc415e8e.databases.neo4j.io:7687"
username = "neo4j"
password = "suzSdYgWm9FkzztWHZXIExxv6kR9WoDzZeIVq8DgfOE"
driver = GraphDatabase.driver(uri, auth=(username, password))
find_active_US_airlines()
# find_cities_reachable_within_d_hops(driver)

# with driver.session() as session:
#     result = session.run("MATCH(n:Airline) RETURN n")
#     for record in result:
#         print(record[0]['Airline ID'])

    # driver.close()