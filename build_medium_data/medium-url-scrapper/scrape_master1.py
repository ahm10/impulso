# medium url scrapper main file
import os
from mediumURLscraper import *
import pandas as pd
#TO RUN THIS FILE YOU NEED SELENIUM, BEAUTIFULSOUP, PANDAS, DATETIME, REGEX, AND OS
#JUST GO TO THE COMMAND LINE AND
#SET WORKING DIRECTORY TO THE DIRECTORY WITH BOTH MEDIUM_SCRAPER.PY AND SCRAPE_MASTER.PY
#THEN ENTER COMMAND "$python scrape_master.py"


#ADD THE TAGS TO SCRAPE HERE
#'r','python', 'data-science','machine-learning', 'artificial-intelligence','deep-learning',data-engineering', 'data-analytics', 'statistics', 'reinforcement-learning'
# tags = ['reinforcement-learning']

# read list of topics to scrap
path_to_topic_index = '../../topics_index/'

topic_index_file = path_to_topic_index + "topics_list.csv"

tags_df = pd.read_csv(topic_index_file)

tags = tags_df['Title']

#ADD THE DATES TO SCRAPE HERE
yearstart=2020
monthstart=7
yearstop=2016
monthstop=1

#LOOPS THROUGH ALL LISTED-TAGS AND SCRAPES DATA OFF OF MEDIUM/TAG/archive
#SAVES THE FILES TO /TAG_SCRAPES/ IN CSV FORMAT
for tag in tags:
    tag = tag.lower().replace("_","-") # for medium format
    scrape_tag(tag, yearstart, monthstart, yearstop, monthstop)
    print("Done with tag: ", tag)
print("done")
