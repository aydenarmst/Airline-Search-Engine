from neo4j import GraphDatabase
import json

def execute_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        return result



uri = "neo4j+s://fc415e8e.databases.neo4j.io:7687"
username = "neo4j"
password = "suzSdYgWm9FkzztWHZXIExxv6kR9WoDzZeIVq8DgfOE"
driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("MATCH(n:Airline) RETURN n")
    for record in result:
        print(record[0]['Airline ID'])

    driver.close()