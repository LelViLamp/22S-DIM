#!/usr/bin/python3

import psycopg2 as pg2

"""
INSTRUCTION TASK 4:
write a small Python3 application. We recommend to use the psycopg2 module (or driver) for 
Python3 to (a) establish a connection to your local database, (b) execute the queries and 
retrieve the results, and (c) close the connection to your local database. Your application 
should execute the queries Q1, Q2, and Q4 as provided in Section 2.3 and print the respective 
results (i.e., all the tuples that are returned by PostgreSQL; output format does not matter 
as long as it is human-readable).
"""

# Credentials
dbname = 'assignment1'
username = 'dbtutorial'
password = 'dbpwd1'

# Some helper function
def print_records(records: list[tuple]):
    if records is None:
        print("The result list is None.")
        return
    print(f"{len(records)} record",
          "s were" if len(records) != 1 else " was",
          " found",
          sep="")
    for record in records:
        print(record)
def state_query(query : str, qid : str = '', offset_line : bool = True):
    if offset_line: print()
    print(f"Executing query",
          f" {qid}" if qid != '' else '',
          ": ",
          query,
          sep='')

# Execute file from shell
if __name__ == "__main__":
    try:
        connection = pg2.connect(f"dbname='{dbname}' user='{username}' password='{password}'")
    except:
        print("Unable to connect to database. R U even interweb?")
    
    cursor = connection.cursor()

    try:
        # Q1, Q2 & Q4
        queries = {
            'q1': "SELECT * FROM names WHERE primaryName = 'Chris Hemsworth';",
            'q2': "SELECT * FROM titles WHERE primaryTitle = 'The Avengers' AND titleType = 'movie';",
            'q4': "EXPLAIN SELECT * FROM titles WHERE primaryTitle = 'The Avengers' and titleType = 'movie';"
        }
        for qid in queries:
            query = queries[qid]
            state_query(query, qid)
            cursor.execute(query)
            records = cursor.fetchall()
            print_records(records)
        
        # TODO q4 could be printed more nicely not as tuples (each row of execution plan is a tuple) but as 
        
        # Q3
        qid = "q3"
        query = "SELECT primaryTitle FROM names, titles WHERE names.birthYear = titles.startYear AND names.primaryName = 'Scarlett Johansson';"
        state_query(query, qid)
        cursor.execute(query)
        counter = cursor.rowcount
        print(f"We found {counter} film",
              "s" if counter != 1 else "",
              " that were published in the year Scarlett was born.",
              sep="")
        
    except:
        print("Exception while executing the query.")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# ok, bye!
