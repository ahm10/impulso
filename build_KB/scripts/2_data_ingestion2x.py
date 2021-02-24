
'''
Objective: Collect wikidata and ingest in grakn schema.
Run from the root
$ python ./build_KB/scripts/2_data_ingestion2x.py
$ python ROOT_DIR/WIKI_DIR/SCRIPTS_DIR/filename.py

'''


### GET PATHS FROM UNIVERSAL CONFIG

import configparser


config = configparser.ConfigParser()
config.read('config.ini')
ROOT_BASE_DIR_PATH = config['ROOT_PATH']['basedir']
WIKI_BASE_DIR_PATH = ROOT_BASE_DIR_PATH + config['WIKI_PATHS']['basedir']
WIKI_DATASTORE_PATH = WIKI_BASE_DIR_PATH + config['WIKI_PATHS']['datastoredir']
WIKI_SCRAPPED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['scrapped']
WIKI_PARSED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['parsed']
WIKI_STRUCTURED_PATH = WIKI_DATASTORE_PATH + config['WIKI_PATHS']['structured']

MEDIUM_BASE_DIR_PATH = ROOT_BASE_DIR_PATH + config['MEDIUM_PATHS']['basedir']
MEDIUM_DATASTORE_PATH = MEDIUM_BASE_DIR_PATH + config['MEDIUM_PATHS']['datastoredir']
MEDIUM_SCRAPPED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['scrapped']
MEDIUM_PARSED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['parsed'] # for title etc
MEDIUM_STRUCTURED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['structured'] # for content



# from grakn.client import GraknClient
import grakn_utils
import csv
import pandas as pd
import json
import os
import numpy as np
import math
import utils

parsed_files = os.listdir(WIKI_PARSED_PATH)

 
#### recording all URLS to make sure no redundancy 

child_ids = []
parent_ids = []

med_cols = ['Title', 'Author','url','Tag','Claps','Comment']
med_ingest_cols = ['Title', 'Author','url']
n_articles = 50
n_topics = 5
for filename in parsed_files:
    # print("Collecting data from...",filename)


    try:
        topic_to_do = filename.split(".json")[0]
        print("topic_to_do--",topic_to_do)


        ### MEdium data collection

        med_path = MEDIUM_PARSED_PATH + topic_to_do + ".csv"
        with open(med_path): 
            df = pd.read_csv(med_path,usecols=med_cols)

            # print("No. of articles (Before cleaning) : ",len(df) )

            # treat mixed data types
            df = utils.med_data_clean(df)

 ######################### NOTE: please uncomment this to collect all articles. WARNING: It is compute intensive.

            # n_articles = len(df) # by default take all
            topic_articles_data = df.loc[:n_articles,med_ingest_cols].to_dict(orient='records')
    
    
    
        ## get conts for topics from wiki

        

        with open(WIKI_PARSED_PATH + topic_to_do +".json") as f1:
            cont = json.load(f1)
            cont_keys = cont.keys()

        ## get the tree structure for indexing

        print("---DATA COLLECTION FOR " + topic_to_do + " ------")
        cols = ['child','parent','rel_level']
        wiki_tree_structure = pd.read_csv(WIKI_STRUCTURED_PATH + topic_to_do +".csv")

        # print("wiki_tree_structure  ",wiki_tree_structure.head())
        

        ent_key = ['Tparent','Tchild','article']
        rel_key = ['ConsistsOf','ExplainedIn']     

        n = len(wiki_tree_structure)

        keys = ent_key + rel_key
        
        D = dict(zip(keys,[]))

        for key in keys:
            D[key] = []

        # print(D)

        ###### WIKI ingestion
        # # organize each item 

        ### 
        # n = 2 # no of branches to include, by default all
        for k in range(n):


            content = ''
            if (wiki_tree_structure.loc[k,'child'] in cont.keys()):
                content += cont[wiki_tree_structure.loc[k,'child']]

            new_parent = wiki_tree_structure.loc[k,'parent']

            new_child = wiki_tree_structure.loc[k,'child']

            topic_to_do_formatted = grakn_utils.process_topic_names(topic_to_do)

            new_parent_formatted = grakn_utils.process_topic_names(wiki_tree_structure.loc[k,'parent'])

            new_child_formatted = grakn_utils.process_topic_names(wiki_tree_structure.loc[k,'child'])

            new_parent_unformatted = grakn_utils.reverse_process_topic_names(wiki_tree_structure.loc[k,'parent'])

            new_child_unformatted = grakn_utils.reverse_process_topic_names(wiki_tree_structure.loc[k,'child'])

            url_parent = grakn_utils.fetch_URL(topic_to_do_formatted,new_parent_formatted)
    
            url_child = grakn_utils.fetch_URL(topic_to_do_formatted,new_child_formatted)

            uuid_parent = grakn_utils.get_uuid(url_parent) # generate uuid

            uuid_child = grakn_utils.get_uuid(url_child)

            if (topic_to_do==new_parent): 
                topic_to_do_UUID = uuid_parent

            # by default false
            is_new_parent = False

            is_new_child = False

            d1 = int(wiki_tree_structure.loc[k,'rel_level'])
            
            d2 = d1 + 1


            if (uuid_parent not in parent_ids): # enter a new parent topic

                ent_type = 'Tparent'

                is_new_parent = True

                parent_ids.append(uuid_parent)

                new_topic = {'UUID': uuid_parent ,'title':new_parent_formatted, 'URL' : url_parent,'path_depth': str(d1)}

                D[ent_type].append(new_topic)


            if (uuid_child not in child_ids): # enter a new child topic

                ent_type = 'Tchild'

                is_new_child = True

                child_ids.append(uuid_child)

                new_topic = {'UUID':uuid_child,'title':new_child_formatted, 'URL' : url_child,'path_depth': str(d2)}

                D[ent_type].append(new_topic)

                # build the relation

            

            ConsistsOfID =  grakn_utils.generate_ConsistsOfID(wiki_tree_structure.loc[k,:])

            new_rel = {'ConsistsOfID' : ConsistsOfID, 'parent': new_parent_formatted, 'child':new_child_formatted,'content': content}

            rel_type = 'ConsistsOf'

            D[rel_type].append(new_rel)


        ###### Medium data ingestion

        print("Ingesting medium data for ", topic_to_do)

        ent_type = 'article'

        rel_type = "ExplainedIn"

        for article in topic_articles_data: 
            med_content = ''
            med_child = ''
            D[ent_type].append(article)
            article["UUID"] = grakn_utils.get_uuid(article['url'])
            ExplainedInID = grakn_utils.generate_ExplainedInID(topic_to_do,article['url'])
            new_rel = {'ExplainedInID' : ExplainedInID, 'parent': topic_to_do_UUID,'supplement':article["UUID"],'content': med_content}
            # print(new_rel)
            D[rel_type].append(new_rel)

            
        # print("------------------------------------------------")
        # print(D)


        # create inputs 
        inputs = grakn_utils.create_inputs()

        # Build the graph (refer grakn utils to understand the entire flow)
        grakn_utils.build_impulso_graph(inputs=inputs,D=D)


    except: 
        pass