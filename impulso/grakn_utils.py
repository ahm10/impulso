from grakn.client import GraknClient
import csv
import pandas as pd
import json
import os


 
# def process_topic_names(topicname):
#     return topicname.replace(' ','_')

# def reverse_process_topic_names(topicname):
#     return topicname.replace('_',' ')

def fetch_URL(topic,child):

    url = 'https://en.wikipedia.org/wiki/' + topic
    if topic!=child:
        url = url + "#" + child

    return url
    
def check_entered(val,listofdict):
    for d in listofdict:
        if (val == d["title"]):
            return False
    return True
    
    
def build_impulso_graph(inputs, D):
        with GraknClient(uri="localhost:48555") as client:
            with client.session(keyspace = "impulso2") as session:
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



def Tparent_template(topic):
        #print(topic)
        q = 'insert $topic isa Tparent, has title ' + '"' +  topic["title"] + '"' + ', '  +' has URL ' + '"' + topic["URL"] + '" '  + ';'
        
        #print(">> ",q)
        # q= 'insert $topic isa topic,'  
        # q+= ' has title "' + topic["title"] + '",'
        # q+= ' has txt "' + topic["txt"] + '"'
        # q+= ' ;'

        return q

def Tchild_template(topic):
        #print(topic)
        q = 'insert $topic isa Tchild, has title ' + '"' +  topic["title"] + '"' + ', '  +' has URL ' + '"' + topic["URL"] + '" '  + ';'
        
        #print(">> ",q)
        # q= 'insert $topic isa topic,'  
        # q+= ' has title "' + topic["title"] + '",'
        # q+= ' has txt "' + topic["txt"] + '"'
        # q+= ' ;'

        return q




def ConsistsOf_template(rel1):
        # match parent
        graql_insert_query = 'match $topic1 isa Tparent, has title "' + rel1["parent"] + '";'
        # match child
        graql_insert_query += ' $topic2 isa Tchild, has title "' + rel1["child"] + '";'
        # insert rel
        graql_insert_query += " insert (parent: $topic1, child: $topic2) isa ConsistsOf,"

        graql_insert_query += ' has content "' + rel1["content"] + '";'
        return graql_insert_query



def create_inputs():

    inputs = [
        {
            "name" : "Tparent",
            "template": Tparent_template
        },

        {
            "name" : "Tchild",
            "template": Tchild_template
        },


        {
            "name" : "ConsistsOf",
            "template": ConsistsOf_template
        },


    ]

    return inputs

