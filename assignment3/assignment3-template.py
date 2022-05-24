#!/usr/bin/python3

from neo4j import GraphDatabase, basic_auth
# A module that formats the output in a readable format
import pprint

# A function that takes a transaction object "tx" as first parameter and a 
# cypher_query as second parameter. The Cypher query is then executed (run) 
# using the transaction object and the retrieved data is returned as result.
def get_result(tx, cypher_query):
  return tx.run(cypher_query).data()

def main():
  try:
    # The string that is used to connect to the Neo4j server. In this case, we
    # use the "bolt" connection, which has a different default port (7687) 
    # compared to the web-based graphical user interface (which has default 
    # port 7474).
    connection_string = "bolt://localhost:7687"

    # Establish a connection to the local Neo4j server with the default
    # credentials.
    driver = GraphDatabase.driver(connection_string, auth=basic_auth("neo4j", "dbpwd1"))
  except:
    print("Unable to connect to {}".format(connection_string))

  try:
    # Create a Cypher query (result size limited to 10) 
    cypher_query = '''
      MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 10
    '''

    # Create a session (i.e., context) for the transactions to be executed.
    session = driver.session(database="neo4j")

    # Execute a read transaction based on the give cypher_query and the given 
    # function (get_result). read_transaction takes a function as parameter 
    # (get_result) that in turn takes a transaction object as parameter (cf. 
    # "tx" in the definition of get_result). The cypher_query parameter is then
    # passed to the corresponding transaction "tx" in the "get_result" function.
    result = session.read_transaction(get_result, cypher_query)

    # For interested students:
    # Advanced lambda-based version to get the result of a Cypher query.
    # results = session.read_transaction(
    #   lambda tx: tx.run(cypher_query))

    # Print the result set to the command line. We use the pprint module to 
    # print the result in a (more or less) human-readable format (the standard 
    # print function prints the result in a single line). It is up to you 
    # whether you want to use pprint or not.
    for entry in result:
      pprint.pprint(entry)
  except Exception as e:
    print("Unable to execute simple MATCH query: {}".format(e))
  finally: # The finally - branch is executed independently of an exception.
    if session is not None:
      # Close the session.
      session.close()

    if driver is not None:
      # Close the connection.
      driver.close()

if __name__ == "__main__":
  main()