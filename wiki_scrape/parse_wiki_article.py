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
nlp = English()
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)


pd.set_option('display.max_colwidth', 200)

def sentencizer(text):
    doc = nlp(text)

    sents_list = []
    for sent in doc.sents:
        sents_list.append(sent.text)

    return sents_list

def cleanup(text):
    processed = text.lower()  
    processed = re.sub('[^a-zA-Z]', ' ', processed )  
    processed= re.sub(r'\s+', ' ', processed)

    return processed

# import wikipedia sentences
filename =   "wiki_content_Regression_analysis.json"
candidate_sentences = pd.read_json("scrapped_data/" + filename)
base_full_text = candidate_sentences.fulltext[1]

print("length of base text", len(base_full_text))

N = 25000

print("considering ",N, "words for testing")

base_full_text = base_full_text[:N]

print("slicing paras")

para_list = base_full_text.split('\n\n')

print("No. of paras", len(para_list))

print("------------")

print("slicing headers and paras")
 
headings = [] 
cont = []
remaining = ''
for para in para_list:
    

    combined = para.split("\n")

    heading = combined[0]

    if(':' in heading):
        [heading,remaining] = heading.split(':')
      

    if(len(combined[0]) > 200): 
        heading = 'General'
    

    # process content into sentences
    sub_cont = sentencizer(remaining + combined[-1])

    cont.append(sub_cont) # add additional description into content
    headings.append(heading)


combined_dict = dict(zip(headings,cont))


# second level parting within content
# newheadings = []
# newcontents = []
# for head,sent_list in combined_dict.items():

    
#     for sent in sent_list:
        
#         if(":" in sent):

#             [newheading,newcontent] = sent.split(':')
#             newheadings.append(newheading)
#             newcontents.append(newcontent)
            

# extra = dict(zip(newheadings,newcontents))                

# # add new ones in dict

# combined_dict.update(extra)

opfile = './parsed_data/' + "parsed_" + filename

with open(opfile, 'w') as f:
    json.dump(combined_dict, f)
    

    
