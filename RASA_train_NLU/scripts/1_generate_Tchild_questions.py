'''
Objective: 
To construct structured tree from wiki topics and content.

Run from the root
$ python ./RASA_train_NLU/scripts/1_generate_topic_questions.py
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
RASA_TRAIN_PATH = ROOT_BASE_DIR_PATH + config['RASA_TRAIN_PATHS']['basedir']
RASA_TRAIN_DATASTORE_PATH = RASA_TRAIN_PATH + config['RASA_TRAIN_PATHS']['datastoredir']


import spacy
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import glob
import itertools
nlp_blank = spacy.blank('en')
from spacy.matcher import PhraseMatcher
import os
import numpy as np

### name of topics to be constructed tree for (would be replaced with unique tags sets later) 

# topics = ['Machine_learning','Supervised_learning','Regression_analysis']

t = 0

entity_pairs_list = []
relations_list = []

#### Get list of topic questions
q_path = RASA_TRAIN_DATASTORE_PATH + "question_templates_topic_defination.csv"
topic_q_df = pd.read_csv(q_path)

topic_q_list = topic_q_df['questions']

topic_qs = dict()

direct_children_qs = dict()

direct_children_seq = dict()

q_seq_file = RASA_TRAIN_DATASTORE_PATH + "TchildQs.txt"
      
for filename in os.listdir(STRUCTURED_PATH): 

    # topic = topics[t]
    topic = filename.split(".csv")[0]
    print("\n---",topic,"---") 
    print("constructing....")

    topic_qs[topic] = []

    direct_children_qs[topic] = []

    direct_children_seq[topic] = []

    t = t + 1 

### read topic tree
    topic_tree_df = pd.read_csv(STRUCTURED_PATH + filename)

    direct_children = topic_tree_df['parent'] == topic

    direct_children_df = topic_tree_df[direct_children]

    # make direct children questions 

    for child in direct_children_df['child']: 


        for topic_q in topic_q_list:


            new_q = topic_q.replace('X', child)
            new_q = new_q.replace('Tparent','Tchild')

            direct_children_qs[topic].append(new_q)

            new_q = topic_q.replace('X', child)
            new_q = new_q.replace('Tparent','Tchild')

            if (new_q not in direct_children_qs[topic]):

                direct_children_qs[topic].append(new_q)
     


    with open( q_seq_file, 'w') as f1:

        for item in direct_children_qs[topic]:
            f1.write("%s\n" % item)
        

    

        


        
# print(topic_qs)