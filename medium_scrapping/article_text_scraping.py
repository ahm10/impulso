import requests
import re
import time
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import shortuuid 
import json


def is_English(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def clean_string(a_string):
    new_string = re.sub(r'‘|’|"|—|“|”|,', '', a_string).strip()
    new_string = re.sub(r'–', ' ', new_string)
    #new_string = re.sub(r'é', 'e', new_string)
    return new_string

def filter_string(a_string):
    if a_string == '.':
        return False
    elif a_string == '':
        return False
    else:
        return True
    
def get_uuid(url):

    # GENERATE A UNIQUE ID BASED ON THE URL
    
    unique_id = shortuuid.uuid(name=url)
      
    return unique_id

class medium_article_scrapping():
    """
    CLASS DEFINITION TO SCRAPE ALL DATA FOR AN ARTICLE AND RETURN JSON OUTPUT.
    """
    
    def __init__(self):
        self.scraper_class = 'medium_article_scrapping' 
        
     
      
    def get_title(self, soup):
        try:
            title = soup.find('h1').text
            return title
        
        except:
            print("Couldn't get title from article.")
        
    def get_subtitle(self, soup):
        try:
            subtitle_soup = soup.find('h1').parent.parent.next_sibling.find('h2')
            subtitle = clean_string(subtitle_soup.text)
            return subtitle
        
        except:
            print("Couldn't (or didn't) get subtitle from article.") 
            return 'None'
            
    def get_tags(self, soup):
        try:
            tags = []
            tags = [x.text for x in soup.find_all("a", href=re.compile(".*tag.*"))]
            if len(tags) == 0:
                return 'None'
            else:
                return tags
            
        except:
            print("Couldn't get article tags.")
    
    def get_author(self, soup):
        try:
            author = soup.find('div',style=re.compile(r'flex:.*')).find('a').text
            return author
        except:
            print("Couldn't get author from article.")
            
    def get_h1_headers(self, soup):
        try:
            article_soup = soup.find('article')
            h1_header_soups = article_soup.find_all('h1')
            
            if len(h1_header_soups) == 1:
                return 'None'
            else:
                h1_headers = [clean_string(x.text) for x in h1_header_soups[1:]]
                return h1_headers
        except:
            print("Couldn't get h1 headers.")
            
    
    def get_h2_headers(self, soup):
        try:
            h2_headers = []
            
            article_soup = soup.find('article')
            h2_header_soups = article_soup.find_all('h2')
            
            for header_soup in h2_header_soups:
                if header_soup.text == "Dive in. We'll learn what you like along the way.":
                    continue
                else:
                    h2_headers.append(clean_string(header_soup.text))
            
            if len(h2_headers) == 0:
                return 'None'
            else:
                return h2_headers
        
        except:
            print("Couldn't get h2 headers.")
            
    def get_paragraphs(self, soup):
        try:
            article_soup = soup.find('article')
            paragraphs = [clean_string(x.text) for x in article_soup.find_all('p')]
            return paragraphs
        except:
            print("Couldn't scrape paragraphs.")
            
    def get_blockquotes(self, soup):
        try:
            article_soup = soup.find('article')
            blockquotes = [x.text for x in article_soup.find_all('blockquote')]
            return blockquotes
        except:
            print("Couldn't (or didn't) find blockquotes.")
            return 'None'
            
    def get_bolded(self,soup):
        try:
            article_soup = soup.find('article')

            bolded = [x.text.strip() for x in article_soup.find_all('strong')]
            bolded = [clean_string(x) for x in bolded if filter_string(x)]
            bolded = [x for x in bolded if x]
          
            if len(bolded) == 0:
                return 'None'
            else:
                return bolded
        except:
            print("Couldn't get bolded text.")
    
    def get_italics(self, soup):
        try:
            article_soup = soup.find('article')
            italics = [x.text.strip() for x in article_soup.find_all('em')]
            italics = [clean_string(x) for x in italics if filter_string(x)]
            
            if len(italics) == 0:
                return 'None'
            else:
                return italics
        except:
            print("Couldnt get italicized text.")
            
    def count_bullet_lists(self, soup):
        try:
            article_soup = soup.find('article')
            return len(article_soup.find_all('ul'))
        
        except:
            print("Couldn't count bullet lists.")
            
    def count_numbered_lists(self, soup):
        try:
            article_soup = soup.find('article')
            return len(article_soup.find_all('ol'))
        
        except:
            print("Couldn't count numbered lists.")
            
    def count_figures(self, soup):
        try:
            article_soup = soup.find('article')
            figures = article_soup.find_all('figure')
            return len(figures)
        
        except:
            print("Couldn't count images.")  
            
    def count_gists(self, soup):
        try:
            gists = []
            article_soup = soup.find('article')
            for fig in article_soup.find_all('figure'):
                gist_soup = fig.find('iframe', title=re.compile('.*\.py'))
                if gist_soup == None:
                    continue
                else:
                    gists.append(gist_soup)
                    
            return len(gists)
        
        except:
            print("Couldn't count gists.")
            
    def count_code_chunks(self, soup):
        try:
            article_soup = soup.find('article')
            code_chunk_soups = article_soup.find_all('pre')
            return len(code_chunk_soups)
        
        except:
            print("Couldn't count code chunks.")
            
    def count_vids(self, soup):
        try:
            yt_vids = []
            article_soup = soup.find('article')
            for figure in article_soup.find_all('figure'):
                yt_soup = figure.find('iframe', src=re.compile('.*youtube.*'))
                if yt_soup == None:
                    continue
                else:
                    yt_vids.append(yt_soup)
                    
            return len(yt_vids)
                    
        except:
            print("Couldn't get YouTube videos.")        
            
    def count_links(self, soup):
        try:
            article_soup = soup.find('article')
            link_soups = article_soup.find_all('a', {'target': '_blank'})
            return len(link_soups)
        
        except:
            print("Couldn't count links.")      
            
    def scrape(self, url,topic,soup):
        article_data = {
            
            "UUID" : get_uuid(url),
            "url" : url,
            "topic" : topic,
            "title": self.get_title(soup),
            "subtitle": self.get_subtitle(soup),
            "tags": self.get_tags(soup),
            "author": self.get_author(soup),
            "h1_headers": self.get_h1_headers(soup),
            "h2_headers": self.get_h2_headers(soup),
            "paragraphs": self.get_paragraphs(soup),
            "blockquotes": self.get_blockquotes(soup),
            "bold_text": self.get_bolded(soup),
            "italic_text": self.get_italics(soup),
           # "n_figures": self.count_figures(soup),
           # "n_bullet_lists": self.count_bullet_lists(soup),
           # "n_numbered_lists": self.count_numbered_lists(soup),
           # "n_gists": self.count_gists(soup),
           # "n_code_chunks": self.count_code_chunks(soup),
           # "n_vids": self.count_vids(soup),
           # "n_links": self.count_links(soup),
        }
        
        # if subtitle exists, remove it from h2_headers list
        subtitle = article_data['subtitle']
        if subtitle != 'None':
            article_data['h2_headers'].remove(subtitle)
            
            if len(article_data['h2_headers']) == 0:
                article_data['h2_headers'] = 'None'
                
        return(article_data)

# LOAD CSV AND FETCH ARTICLE URLS TO BE SCRAPPED
url_file_name = "Medium_Scrapermedium_data-science"
url_file = url_file_name + ".csv"
urls_df = pd.read_csv(url_file)
# df.head()
# N = no of articles to be scrapped
#N = 2
N = len(urls_df)
# MAKE LISTS
urls = urls_df.url.to_list() 
topics = urls_df.Tag.to_list()
#scrape_urls = urls[:N]

# scrape_urls

# SCRAPE TEXT DATA FROM INDIVIDUAL URL/ARTICLE
# page_url = urls[3]
# driver = webdriver.Chrome()
# driver.get(page_url)
# time.sleep(3)
# soup = BeautifulSoup(driver.page_source, 'lxml')

content = medium_article_scrapping()
# data = content.scrape(soup)
# content_df = pd.DataFrame(columns = list(data.keys()))
# content_df = return_df.append(data, ignore_index=True)
# driver.close()

# SCRAPE FOR MULTIPLE/ALL URLS
content_df = pd.DataFrame(columns = ['UUID', 'url','topic','title', 'subtitle','tags', 'author', 'h1_headers', 'h2_headers', 'paragraphs', 
                                     'blockquotes', 'bold_text', 'italic_text', 
                                     #'n_figures',
                                     #'n_bullet_lists',
                                     #'n_numbered_lists', 
                                     #'n_gists', 
                                     #'n_code_chunks', 
                                     #'n_vids', 
                                     #'n_links'
                                     ])

for article_i in range(N):   

    url = urls[article_i]
    topic = topics[article_i]
    print("Scrapping : ", url)
    #print(topic)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    data_scrape = content.scrape(url,topic,soup)
 
    
    content_df = content_df.append(data_scrape, ignore_index=True,  sort=False)

    driver.close()

print('Scraping done!')
      
# SAVE SCAPED DATA TO CSV

output_file = 'contents_op_' + url_file
content_df.to_csv(output_file, index=False)

# Convert to JSON 
json_file = url_file_name + ".json"
print("writing into..",json_file)
content_df.to_json(json_file,orient="records",force_ascii=False)
print("completed!")
#parsed_content = json.loads(content_df_json)
#op_json = json.dumps(parsed_content,indent=4)    
#print("JSON....")

#print(op_json)
