# Wiki Scrapper   

## Data dictionary (output JSON):   

1. URL : URL of the article
1. tag : the topic of article
1. sections : levelled list of sections
1. full_text : entire text body


## Steps
- Folder : wiki_scrape
- Script to run: single_article_with_category_levels.py
- Settings in script: List of tags to scrap. Please add all the tags you want in this list. 
- Or you can also use CSV read. The code is added with a sample ML.CSV. You would need to place the CSV in the same folder and specify the CSV name inside the script under the variable filename. :heavy_check_mark:
- Output data: A JSON containing above mentioned attributes. You can review example file - wiki_content_Machine learning.json




# Medium_Scraper  

## Data dictionary (output columns):

1. UUID : Universally unique identifier created for each article URL	
1. url : Article URL	
1. topic : Main topic or key word e.g. Data science / Artificial intelligence / ..	
1. title : Title of the article	
1. subtitle	: If available, subtitle for further emphasis on the article's theme
1. tags	: associated tags which are covered in the article
1. tag_links : links underlying the tags  
1. author	: list of writers
1. h1_headers : List of first level headings	
1. h2_headers	: List of second level headings
1. paragraphs : List of paragraphs (each paragraph is a separate entity of 2-5 sentences generally)	
1. blockquotes	: Quotes used by the writers
1. bold_text	: List of important sentances 
1. italic_text : List of codes or special terms as highlighted by writers
1. figures : List of 'full-size' image URLs   
1. links : List of internal reference links in the article  
1. external_links : List of links that point outside medium or its partner websites   


## Steps


### 1. Collect URLS from medium
- Folder : medium-url-scraper
- Script to run: scrape_master.py
- Settings in script: You can change the tag and timeline.

### 2. Remove redundent URLs and further cleaning: 
Same URL could be found multiple times, under multiple different tags. 
There are two sub folders for 2009-16 and 2016-20.
- Folder : Medium_scrape_URL_cleaning_EDA
- Scripts to run: Go in the corresponding folder and you will see a jupyter notebook (e.g. data_cleaning_2016-2020.ipynb)
- Raw data : in folder scraped_tags
- Final output: Single CSV for that time period (e.g. Medium_scrape_urls_multi-tag _clean_2016-2020.csv)

### 3. Scrap body and image URLS 
- Folder : Medium_scrape_text_and_image
- Script to run : article_text_img_scraping.py
- Input data: Please place cleaned csv- as generated on 2nd step. (e.g. Medium_scrape_urls_multi-tag _clean_2016-2020.csv)
- Output data: contents_op_*.csv

:high_brightness: New copy of sample articles are scrapped. 

Please refer : contents_op_Medium_scrape_urls_multi-tag _clean_2016-2020.csv [csv](https://github.com/ahm10/impulso/blob/master/Medium_scrape_text_and_image/2016-2020/contents_op_Medium_scrape_urls_multi-tag%20_clean_2016-2020.csv)


*P.S.*
:memo:


-requirements.txt is available for the environment setup. Please ensure  correct version of chrome driver in respective folders.


-You can also refer instance setup file - example in Medium_scrape_text_and_image folder.


# Neo4j-wiki

1. Neo4j sandbox is implemented.

2. Exported graph and JSON are available for review.

3. It is command line interface like SQL. So do not have instructions listed at the moment.

# Medium - preprocess

## Extract unique tags - steps 

- Folder : Medium_data_preprocess
- Script to run: unique_tags.py
- Settings in script: The script reads content files from the adjacent "data" folder. So please make sure all content files you want to process are placed in there. 
- Output data: All unique tags with their total occurances have been logged into a CSV file in "op" folder.

## Article content preprocessing :heavy_check_mark:
This includes- 
1. Cleaning,

2. Organizing 

3. Breaking it down into sentences. 

- Folder : Medium_data_preprocess
- Script to run: parse_articles.py
- Settings in script: The script reads content files from the adjacent "data" folder. So please make sure all content files you want to process are placed in there. 
- Output data: All articles with thier UUID and sentences (in list form) have been logged into a CSV file in "op" folder in file name parsed_*...csv
*P.S.* For environment setup, use the requirements.txt available in given folder.
:point_right: Special instructions (if required) for spacy installment also attached in txt file besides requirements.txt

 