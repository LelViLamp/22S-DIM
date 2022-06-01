#!/usr/bin/python3

from neo4j import GraphDatabase, basic_auth
# A module that formats the output in a readable format
import pprint

# A function that takes a transaction object "tx" as first parameter and a 
# cypher_query as second parameter. The Cypher query is then executed (run) 
# using the transaction object and the retrieved data is returned as result.
def get_result(tx, cypher_query):
  return tx.run(cypher_query).data()

def insert_director(tx, directorName, movieTitle):
    tx.run("CREATE (b:Person { name : $name }) "
           "WITH b "
           "MATCH (m:Movie { title : $title }) "
           "CREATE (b)-[r:DIRECTED]->(m)",
           name=directorName, title=movieTitle)

def main():
  try:
    # The string that is used to connect to the Neo4j server. In this case, we
    # use the "bolt" connection, which has a different default port (7687) 
    # compared to the web-based graphical user interface (which has default 
    # port 7474).
    connection_string = "bolt://localhost:7687"

    # Establish a connection to the local Neo4j server with the default
    # credentials.
    driver = GraphDatabase.driver(connection_string, auth=basic_auth("neo4j", "hello"))
  except:
    print("Unable to connect to {}".format(connection_string))

  try:
    # Create a Cypher query (result size limited to 10) 
    cypher_query = '''
      MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 10
    '''

    # Create a session (i.e., context) for the transactions to be executed.
    session = driver.session(database="neo4j")

    # Q1, Q2, & Q4
    queries = {
      'q1' : '''
              MATCH (b:Person { name: "Christian Bale" }) -[a1:ACTED_IN]->(m:Movie)<-[a2:ACTED_IN]- (p:Person)
              RETURN b,a1,m,a2,p
              ''',
      'q2' : '''
            MATCH
              p=shortestPath(
                (b:Person { name : 'Christian Bale' })-[*]-(b2:Person { name: 'Halle Berry' })
              )
            RETURN p
            ''',
      'q4' : '''
            MATCH (m:Movie)
            WHERE m.imdbRating >= 9 AND m.year <= 1990
            RETURN m
            '''
    }
    for query in queries:
      print(f"--- {query} ---")
      query = queries[query]
      

      # Execute a read transaction based on the give cypher_query and the given 
      # function (get_result). read_transaction takes a function as parameter 
      # (get_result) that in turn takes a transaction object as parameter (cf. 
      # "tx" in the definition of get_result). The cypher_query parameter is then
      # passed to the corresponding transaction "tx" in the "get_result" function.
      result = session.read_transaction(get_result, query)

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

    # Q3
    print("--- Q3 ---")
    result = session.write_transaction(insert_director, "Daniel Kocher", "Power of Nightmares, The: The Rise of the Politics of Fear")
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