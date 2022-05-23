#!/usr/bin/python3

import pymongo as pym

# A module that formats the output in a readable format, which is quite useful # in case of JSON documents.
import pprint

def main():
    try:
        # Establish a connection to the local MongoDB server without credentials.
        connection = pym.MongoClient("mongodb://localhost")
        
        # If you have credentials, we refer to the documentation for more details:
        # https://pymongo.readthedocs.io/en/stable/examples/authentication.html
    except:
        print("Unable to connect to {}".format('mongodb://localhost'))
    
    try:
        db = connection["assignment2"]
        # Create a dict (aka JSON object) that is used in the find() operation
        
        """
        SAMPLE FROM TEMPLATE
        """
        json_query = {
            "author": "Michael Stonebraker",
            "booktitle": "ICDE"
        }
        
        # Execute the find() operation and retrieve a cursor to the result set
        cursor = db.dblp.find(json_query)

        # Print the documents in the result set to the command line. We use the
        # pprint module to print the JSON document in a human-readable format (the
        # standard print function prints the JSON documents in a single line). It is
        # # up to you whether you want to use pprint or not.
        for i, x in enumerate(cursor):
            pprint.pprint({i: x})
        


        """
        QUERY 1
        db.dblp.find({ 
            "author": "Michael Stonebraker"
        }).pretty()
        """
        json_query = {
            "author": "Michael Stonebraker"
        }
        cursor = db.dblp.find(json_query)
        for i, x in enumerate(cursor):
            pprint.pprint({i: x})
        


        """
        QUERY 2
        db.dblp.find({ 
            "author": "Michael Stonebraker", 
            "booktitle": "ICDE" 
        }).pretty()
        """
        json_query = {
            "author": "Michael Stonebraker",
            "booktitle": "ICDE"
        }
        cursor = db.dblp.find(json_query)
        for i, x in enumerate(cursor):
            pprint.pprint({i: x})
        


        """
        QUERY 3
        db.arxiv.aggregate({
            "$lookup": {
                "from": "dblp",
                "localField": "title",
                "foreignField": "title",
                "as": "arxivdblp"
            }
        }).pretty()
        """
    
        json_query = [
            {
                "$lookup" : {
                    "from": "dblp",
                    "localField": "title",
                    "foreignField": "title",
                    "as": "arxivdblp"
                    }
            },
            { "$count" : "found_after_join" }
        ]
        cursor = db.arxiv.aggregate(json_query)
        for i, x in enumerate(cursor):
            pprint.pprint({i: x})
        


        """
        QUERY 4
        db.dblp.find({ 
            "author": "Michael Stonebraker", 
            "booktitle": "ICDE"
        }).explain()
        """
        json_query = { 
            "author": "Michael Stonebraker", 
            "booktitle": "ICDE"
        }
        cursor = db.dblp.explain(json_query)
        for i, x in enumerate(cursor):
            pprint.pprint({i: x})
    
    except Exception as e:
        print("Unable to execute simple find() query: {}".format(e))
    finally: # The finally-branch is executed independently of an exception.
        if cursor is not None:
            # Close the cursor.
            cursor.close()
        if connection is not None:
            # Close the connection.
            connection.close()

if __name__ == "__main__":
    main()
