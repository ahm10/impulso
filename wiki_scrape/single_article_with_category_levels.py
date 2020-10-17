# import the libraries

import wikipediaapi

import json

import pandas as pd

wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)

sect = []

# utility function for sections tree
def arrange_sections(sections,level=0):   
  
        for s in sections:  
        
          sect.append({str((level + 1)) : s.title})   
        
          #print("%s: %s" % (str((level + 1)), s.title))    
          arrange_sections(s.sections, level + 1)
            

# Please update all the tags you want to scrap for 

#topics = ['Python_(programming_language)','Artificial intelligence','Machine learning']

# alternative code - read from csv
filename = "ML.csv" # place the name of the CSV to be scrapped
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
    
                                        
    filename = "wiki_content_" + topic + ".json" 
    
    # write the content of the topic in the JSON
    
    with open(filename, 'w') as fp:
      json.dump(content, fp)

    



 
 

    
    
  

