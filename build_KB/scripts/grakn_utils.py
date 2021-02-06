from grakn.client import GraknClient
import csv
import pandas as pd
import json
import os
import shortuuid 
import random
from time import sleep
def process_topic_names(topicname):
    return topicname.replace(' ','_').lower().replace('"','`').replace("'","`")

def reverse_process_topic_names(topicname):
    return topicname.replace('_',' ').lower().replace('"','`').replace("'","`")

    
    
def get_uuid(url):

    # GENERATE A UNIQUE ID BASED ON THE URL
    
    unique_id = shortuuid.uuid(name=url)
      
    return unique_id

def generate_ConsistsOfID(row):

    n = row['rel_level']

    child = row['child']

    parent = row['parent']

    parent_child_combo = child + parent

    # generate unique combo based on parent, child and rel level

    ConsistsOfID = str (n) + shortuuid.uuid(name=parent_child_combo)

    return ConsistsOfID
    
def generate_ExplainedInID(t,art):


    parent_art_combo = art + t

    # generate unique combo based on parent, child and rel level

    ExplainedInID = shortuuid.uuid(name=parent_art_combo)

    return ExplainedInID

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
            with client.session(keyspace = "impulso0") as session:
                for input in inputs:
                    print("Loading from [" + input["name"] + "] into Grakn ...")
                    load_data_into_grakn(input, D, session)

def load_data_into_grakn(input, D,  session):
        #items = parse_data_to_dictionaries(input)
        items = D[input["name"]]
        
        for item in items:
            with session.transaction().write() as transaction:
                graql_insert_query = input["template"](item)
                # print("Executing Graql Query: " + graql_insert_query)
                transaction.query(graql_insert_query)
                transaction.commit()
                sleep(0.1)

        print("\nInserted " + str(len(items)) + " items from [ " + input["name"] + "] into Grakn.\n")



def Tparent_template(topic):
        #print(topic)
        q = 'insert $topic isa Tparent, has UUID "' + topic["UUID"] + '"' + ',' + ' has title ' + '"' +  topic["title"] + '"' + ', '  +' has URL ' + '"' + topic["URL"] + '"' + ', '  +' has path_depth ' + '"' + topic["path_depth"] + '" '  + ';'
        
        #print(">> ",q)
        # q= 'insert $topic isa topic,'  
        # q+= ' has title "' + topic["title"] + '",'
        # q+= ' has txt "' + topic["txt"] + '"'
        # q+= ' ;'

        return q

def Tchild_template(topic):
        #print(topic)
        q = 'insert $topic isa Tchild, has UUID "' + topic['UUID'] + '"' + ',' + ' has title ' + '"' +  topic["title"] + '"' + ', '  +' has URL ' + '"' + topic["URL"] + '" '  + ', '  +' has path_depth ' + '"' + topic["path_depth"] + '" '  + ';'
        
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

        graql_insert_query += ' has content "' + rel1["content"] + '", '

        graql_insert_query += ' has ConsistsOfID "' + rel1["ConsistsOfID"] + '";'

        return graql_insert_query


def article_template(article):

        q = 'insert $article isa article, has UUID "' + article["UUID"] + '"' + ',' + ' has title ' + '"' +  article["Title"] + '"' + ', '  +' has URL ' + '"' + article["url"] + '"' + ', '  +' has author ' + '"' + article["Author"] + '" '  + ';'
            


        return q

def ExplainedIn_template(rel2):

        # print("~~~~~~")
        # print(rel2)
        # match parent
        graql_insert_query = 'match $topic1 isa Tparent, has UUID "' + rel2["parent"] + '";'
        # match child
        graql_insert_query += ' $article isa article, has UUID "' + rel2["supplement"] + '";'
        # insert rel
        graql_insert_query += " insert (parent: $topic1, supplement: $article) isa ExplainedIn,"

        graql_insert_query += ' has content "' + rel2["content"] + '", '

        graql_insert_query += ' has ExplainedInID "' + rel2["ExplainedInID"] + '";'

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

        {
            "name" : "article",
            "template": article_template
        },

        {
            "name" : "ExplainedIn",
            "template": ExplainedIn_template
        },



    ]

    return inputs

