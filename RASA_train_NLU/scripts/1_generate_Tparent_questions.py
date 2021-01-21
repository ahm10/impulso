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


###### Note: Ensure that all these topics are scrapped parsed and strctured. 

#topic_list = ["Machine Learning", "Python", "Data Science", "Reinforcement Learning", "Artificial Intelligence"]

structured_topic_list = os.listdir(STRUCTURED_PATH) 

topic_list = []

for t in structured_topic_list: 

  topic = t.split(".csv")[0]
  topic_list.append(t)
  
  

topic_qs = [] 
for topic in topic_list: 


    print("\n---",topic,"---") 
    print("constructing....")

    


    # make topic definition questions

    # pick a random pattern of question


    for topic_q in topic_q_list: 

        new_q = topic_q.replace('X', topic)

        topic_qs.append(new_q)
    


    with open(RASA_TRAIN_DATASTORE_PATH + "TparentQs.txt", 'w') as f:
        json.dump(topic_qs,f)



