

'''
Objective: 
To parse and clean the scrapped wikipedia content.

Run from the root
$ python ./build_wiki_data/scripts/2_parse.py
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


import re
import pandas as pd
import bs4
import os
import requests
import spacy
import wikipediaapi
import json
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from spacy.lang.en import English
nlp = English()
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)
import utils
 

pd.set_option('display.max_colwidth', 200)

def cleanup(text):

    # replace new lines with bullets

    text = text.replace("\n", " \u2022 ")

    # replace quotations with `

    text = text.replace('"', '`')

    text = text.replace("'", '`')

    return text

for sfile in os.listdir(SCRAPPED_PATH):
    file_path = SCRAPPED_PATH + sfile 
    print("Parsing...",file_path)

    with open(file_path) as f:
        data = json.load(f)


    # candidate_sentences = pd.read_json("./scrapped_data/" + filename,orient='records')
    base_full_text = data['fulltext'].split("\n\n")
    sections = data['sections']

    # for s in sections[:2]: 

    #     print(">>>> ",s)

    initial_text = base_full_text[:1]


    rest_text = base_full_text[1:]
    combined = dict()


    combined['introduction'] = cleanup(" ".join(initial_text))

    # retrieve structure
    
    topic = sfile.split(".json")[0]
 

    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)


    pg = wiki_wiki.page(topic)

    headings = []
    for sect in sections:

        s = ''+ list(sect.values())[0]     
        headings.append(s)

    # print(">>",headings)

    for txt in rest_text:

        # print(txt)
        # print("..................")

        h = txt.split("\n")[0]
        t = txt.split("\n")[1:]

        if(t):

            t = " ".join(t)

            # print(t)

            
            # print(".......")
            # print(utils.summarize(t))

            if (h in headings): 

                t =  utils.summarise(t) # summerized text body

                t = cleanup(t) # replace new lines 

                combined[h] = t

    # print("headings in ",topic)    

    # print(len(combined.keys()))
                
 
    #write the combined into json

    opfile = PARSED_PATH +topic+".json" 
    with open(opfile, 'w') as fp:
        json.dump(combined, fp, indent=4)

    print("parsed data + summerized text written in ",opfile)
