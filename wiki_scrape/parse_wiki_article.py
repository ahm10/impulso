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

scrapped_data_path = "./scrapped_data/"
for sfile in os.listdir(scrapped_data_path):
    file_path = scrapped_data_path + sfile 
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
    
    topic = sfile.split("wiki_content_")[-1].split(".json")[0]
 

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

    opfile = "./parsed_data/"+"parsed_"+topic+".json" 
    with open(opfile, 'w') as fp:
        json.dump(combined, fp, indent=4)

    print("parsed data + summerized text written in ",opfile)
