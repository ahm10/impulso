
'''
Objective: Collect wikidata and ingest in grakn schema.
Run from the root
$ python ./build_KB/scripts/2_data_ingestion.py
$ python ROOT_DIR/WIKI_DIR/SCRIPTS_DIR/filename.py

'''


### GET PATHS FROM UNIVERSAL CONFIG

import configparser


config = configparser.ConfigParser()
config.read('config.ini')
ROOT_BASE_DIR_PATH = config['ROOT_PATH']['basedir']
WIKI_BASE_DIR_PATH = ROOT_BASE_DIR_PATH + config['WIKI_PATHS']['basedir']
WIKI_DATASTORE_PATH = WIKI_BASE_DIR_PATH + config['WIKI_PATHS']['datastoredir']
SCRAPPED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['scrapped']
PARSED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['parsed']
STRUCTURED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['structured']


# from grakn.client import GraknClient
import grakn_utils
import csv
import pandas as pd
import json
import os




parsed_files = os.listdir(PARSED_PATH)

 
#### recording all URLS to make sure no redundancy 

URLs = []


for filename in parsed_files:
    print("Collecting data from...",filename)
    topic_to_do = filename.split(".json")[0]
    print("topic_to_do--",topic_to_do)
    # topic_to_do = "Machine_learning"

 
    ## get conts for topics 

    with open(PARSED_PATH + topic_to_do +".json") as f1:
        cont = json.load(f1)
        cont_keys = cont.keys()

    ## get the tree structure for indexing

    print("---DATA COLLECTION FOR " + topic_to_do + " ------")
    cols = ['child','parent','rel_level']
    tree_structure = pd.read_csv(STRUCTURED_PATH + topic_to_do +".csv")

    print("tree_structure  ",tree_structure.head())
    

    ent_key = ['Tparent','Tchild']
    rel_key = ['ConsistsOf']     

    n = len(tree_structure)

    keys = ent_key + rel_key
    print(keys)
    D = dict(zip(keys,[]))

    for key in keys:
        D[key] = []

    print(D)

    # # organize each item 
    for k in range(n):

        content = ''
        if (tree_structure.loc[k,'child'] in cont.keys()):
            content += cont[tree_structure.loc[k,'child']]

        new_parent = tree_structure.loc[k,'parent']

        new_child = tree_structure.loc[k,'child']

        topic_to_do_formatted = grakn_utils.process_topic_names(topic_to_do)

        new_parent_formatted = grakn_utils.process_topic_names(tree_structure.loc[k,'parent'])

        new_child_formatted = grakn_utils.process_topic_names(tree_structure.loc[k,'child'])

        new_parent_unformatted = grakn_utils.reverse_process_topic_names(tree_structure.loc[k,'parent'])

        new_child_unformatted = grakn_utils.reverse_process_topic_names(tree_structure.loc[k,'child'])

        url_parent = grakn_utils.fetch_URL(topic_to_do_formatted,new_parent_formatted)
 
        url_child = grakn_utils.fetch_URL(topic_to_do_formatted,new_child_formatted)

        

        # by default false
        is_new_parent = False

        is_new_child = False

        if (url_parent not in URLs): # enter a new parent topic

            ent_type = 'Tparent'

            is_new_parent = True

            URLs.append(url_parent)

            new_topic = {'title':new_parent, 'URL' : url_parent}

            D[ent_type].append(new_topic)


        if (url_child not in URLs): # enter a new child topic

            ent_type = 'Tchild'

            is_new_child = True

            URLs.append(url_child)

            new_topic = {'title':new_child, 'URL' : url_child}

            D[ent_type].append(new_topic)

        if (is_new_parent or is_new_child): # form a new relation consistsof

            new_rel = {'parent': new_parent, 'child':new_child,'content': content}

            rel_type = 'ConsistsOf'

            D[rel_type].append(new_rel)

        

    # print(D)
 

    # # create inputs 
    inputs = grakn_utils.create_inputs()

    # # Build the graph (refer grakn utils to understand the entire flow)
    grakn_utils.build_zeitlabs_graph(inputs=inputs,D=D)