from grakn.client import GraknClient
import csv
import pandas as pd
import json
import os
import grakn_utils
    
def check_entered(val,listofdict):
    for d in listofdict:
        if (val == d["title"]):
            return False
    return True
    
    
def build_zeitlabs_graph(inputs, D):
        with GraknClient(uri="localhost:48555") as client:
            with client.session(keyspace = "zeitlabs") as session:
                for input in inputs:
                    print("Loading from [" + input["name"] + "] into Grakn ...")
                    load_data_into_grakn(input, D, session)

def load_data_into_grakn(input, D,  session):
        #items = parse_data_to_dictionaries(input)
        items = D[input["name"]]
        for item in items:
            with session.transaction().write() as transaction:
                graql_insert_query = input["template"](item)
                print("Executing Graql Query: " + graql_insert_query)
                transaction.query(graql_insert_query)
                transaction.commit()

        print("\nInserted " + str(len(items)) + " items from [ " + input["name"] + "] into Grakn.\n")

def topic_template(topic):
        #print(topic)
        q = 'insert $topic isa topic, has title ' + '"' +  topic["title"] + '"' + ', '  +' has txt ' + '"' + topic["txt"] + '" '  + ';'
        
        #print(">> ",q)
        # q= 'insert $topic isa topic,'  
        # q+= ' has title "' + topic["title"] + '",'
        # q+= ' has txt "' + topic["txt"] + '"'
        # q+= ' ;'

        return q

def subtopic1_template(subtopic1):
        q = 'insert $subtopic1 isa subtopic1, has title ' + '"' +  subtopic1["title"] + '"' + ', '  +' has txt ' + '"' + subtopic1["txt"] + '" '  + ';'
        return q

def subtopic2_template(subtopic2):
        q = 'insert $subtopic2 isa subtopic2, has title ' + '"' +  subtopic2["title"] + '"' + ', '  +' has txt ' + '"' + subtopic2["txt"] + '" '  + ';'
        return q

def subtopic3_template(subtopic3):
        q = 'insert $subtopic3 isa subtopic3, has title ' + '"' +  subtopic3["title"] + '"' + ', '  +' has txt ' + '"' + subtopic3["txt"] + '" '  + ';'
        return q


def rel1_template(rel1):
        # match topic
        graql_insert_query = 'match $topic isa topic, has title "' + rel1["topic"] + '";'
        # match subtopic1
        graql_insert_query += ' $subtopic1 isa subtopic1, has title "' + rel1["subtopic1"] + '";'
        # insert rel1
        graql_insert_query += " insert (level0: $topic, level1: $subtopic1) isa rel1;"
        return graql_insert_query

def rel2_template(rel2):
        
        # match subtopic1
        graql_insert_query = 'match $subtopic1 isa subtopic1, has title "' + rel2["subtopic1"] + '";'
        
        # match subtopic2
        graql_insert_query += ' $subtopic2 isa subtopic2, has title "' + rel2["subtopic2"] + '";'

        # insert rel2
        graql_insert_query += " insert (level1: $subtopic1, level2: $subtopic2) isa rel2;"
        return graql_insert_query

def rel3_template(rel3):
        
        # match subtopic2
        graql_insert_query = 'match $subtopic2 isa subtopic2, has title "' + rel3["subtopic2"] + '";'  
        
        # match subtopic3
        graql_insert_query += ' $subtopic3 isa subtopic3, has title "' + rel3["subtopic3"] + '";'

        # insert rel3
        graql_insert_query += " insert (level2: $subtopic2, level3: $subtopic3) isa rel3;"
        return graql_insert_query


def create_inputs():

    inputs = [
        {
            "name" : "topic",
            "template": topic_template
        },

        {
            "name" : "subtopic1",
            "template": subtopic1_template
        },
            {
            "name" : "subtopic2",
            "template": subtopic2_template
        },
            {
            "name" : "subtopic3",
            "template": subtopic3_template
        },
        {
            "name" : "rel1",
            "template": rel1_template
        },
        {
            "name" : "rel2",
            "template": rel2_template
        },
        {
            "name" : "rel3",
            "template": rel3_template
        }

    ]

    return inputs

