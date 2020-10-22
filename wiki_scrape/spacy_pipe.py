import re
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
import json
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

# Load spacy langauge model

nlp = spacy.load('en_core_web_sm')

# Getting the pipeline component
ner=nlp.get_pipe("ner")

def get_entities(sent):
 
  #############################################################
  
  for tok in nlp(sent):

    print(">>",tok.text, "=", tok.dep_)


filename = './parsed_data/' + "parsed_wiki_content_Machine learning.json"

with open(filename) as f:
  parsed_data = json.load(f)

# for head,sent_list in parsed_data.items():

#     entity_pairs = []
#     for sent in tqdm(sent_list[:1]): 

#         entity_pairs.append(get_entities(sent))


# print(entity_pairs) 

 
