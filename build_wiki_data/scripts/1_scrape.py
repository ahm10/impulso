
'''
Objective: 
To scrap data from wikipedia based on list of topics or csv (to be uncommented).
Run from the root
$ python ./build_wiki_data/scripts/1_scrape.py
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
TOPICS_LIST_PATH = ROOT_BASE_DIR_PATH + config['TOPICS_LIST_PATH']['basedir']
###################

# import the libraries

import wikipediaapi

import json

import pandas as pd

import os

wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)

sect = []

# utility function for sections tree
def arrange_sections(sections,level=0):   
  
        for s in sections:  
        
          sect.append({str((level + 1)) : s.title})   
        
          #print("%s: %s" % (str((level + 1)), s.title))    
          arrange_sections(s.sections, level + 1)
            
   
# Please update all the tags you want to scrap for 

#topics = ["Machine_learning","Python_(programming_language)","Data_science","Reinforcement_learning","Artificial_intelligence"]

# alternative code - read from csv
filename = TOPICS_LIST_PATH + "topics_list.csv" # place the name of the CSV to be scrapped


tags_df = pd.read_csv(filename)
topics = list(tags_df['title'])



# Scrap all tags one by one and create JSON for each


for topic in topics:

  pg = wiki_wiki.page(topic)
  
  sect = []
  
  if pg.exists():   # if the page is found 

    content = dict()
    
    # collect topic contents


    content['url'] = pg.fullurl

    content['tag'] = topic       
    
    arrange_sections(pg.sections)  
    
    content['sections'] = sect
    
    content['fulltext'] =  pg.text
    
    # create a topic JSON
    
    # store it in data folder
    if '"' in topic:
      topic.replace('"','_')

    if ('*' in topic):
      print('Yes')
      a = topic.split('*')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    if ('?' in topic):
      print('Yes')
      a = topic.split('?')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    

    if ('/' in topic):
      print('Yes')
      a = topic.split('/')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    
    if ('\\' in topic):
      print('Yes')
      a = topic.split('\\')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    
    if (':' in topic):
      print('Yes')
      a = topic.split(':')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    if ('<' in topic):
      print('Yes')
      a = topic.split('<')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    if ('>' in topic):
      print('Yes')
      a = topic.split('>')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    if ('|' in topic):
      print('Yes')
      a = topic.split('|')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
    if (';' in topic):
      print('Yes')
      a = topic.split(';')
      
      topic = ''
      for i in range(len(a)):
        topic = topic + a[i]
                                        
    filename = SCRAPPED_PATH + topic + ".json" 
    
    # write the content of the topic in the JSON
    
    with open(filename, 'w') as fp:
      json.dump(content, fp)
      print("Scrapped data at ",filename)


    



 
 

    
    
  

