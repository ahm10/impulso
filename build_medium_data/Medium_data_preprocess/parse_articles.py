import pandas as pd 
import utils
import re
import glob
import time
import os

 # collect all content files placed in data folder
scraped_files = glob.glob('data/*.csv')

 
# read each file one by one
for file in scraped_files:

  

    #print("Processing...",file)

    #all of the scraped data from different tags
    content_df = pd.read_csv(file,usecols=['UUID','title','paragraphs'],encoding='utf8')
 
    
    print("1. Combining texts like bullet points into one para")
    print("2. Clean up step 1, remove quatations & slice the content into paras")
    print("3. Break down into sentences")

    content_df['sentences'] = ''
   
    for index, row in content_df.iterrows():

        print("..")

        
        #print(index, row['UUID'], row['paragraphs'], row['sentences'])
        paragraphs = row.paragraphs

        
        title = row.title
        
        # 1. Combining texts like bullet points into one para

        # Make sure it is not an empty element

        #check charecters in article with title

        if(utils.check_charecters(str(title))):
            

            # if valid paragraph
            if(paragraphs):

                # Ensure it is english content with SPACY
                if(utils.check_lang(paragraphs)): 

                        UUID = row.UUID

                        # combine lists
                        paragraphs = utils.combiner(paragraphs)
                             
                        paragraphs = paragraphs + ''
                        #print("after combining---------------")
                        #print(paragraphs)
                
                        # 2. Clean up step 1, remove quatations & slice the content into paras
                
                        para_list = utils.preprocess0(paragraphs)

                        #3.Break down into sentences
                        #content_df.at[para_i,'sentences'] = ''
                        for para in para_list:
                            #print(".....")

                            para = utils.preprocess2(para)
                            #print(para)

                            sent_list = utils.sentencer(para)

                            #content_df['sentences'] = content_df['sentences'].astype('object') 
                            #sent_list = ['a','b']
                            mask = (content_df['UUID']==UUID)
                            old = content_df.loc[mask,'sentences']

                            content_df.loc[mask,'sentences']  = old +  ''.join(sent_list) 
 

        orginal_file_name = os.path.basename(file)
        
        data_store_path = './op/'

        op_file = data_store_path + "parsed_" + orginal_file_name
        
        content_df.loc[:,['UUID','sentences']].to_csv(op_file,index=False)

        #print(content_df.head())

        # create clean o/p file

        op_df = pd.read_csv(op_file)

        op_df = op_df.dropna()

        # ensure propoer index
        op_df = op_df.reset_index(drop=True)

        op_df.to_csv(op_file,index=False)



    print("Parsed results in stored in ", op_file)

    

  

    
    
    