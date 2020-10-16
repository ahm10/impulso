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
    #all of the scraped data from different tags
    content_df = pd.read_csv(file,usecols=['UUID','paragraphs'])

    
    print("1. Combining texts like bullet points into one para")
    print("2. Clean up step 1, remove quatations & slice the content into paras")
    print("3. Break down into sentences")

    content_df['sentences'] = ''
    para_i = 0
    for paragraphs in content_df.paragraphs:
        
        
        # 1. Combining texts like bullet points into one para

        # Make sure it is not an empty element

        paragraphs = ' ' + str(paragraphs)

        if(len(paragraphs) > 1):

            print("Processing...",file)
 
            paragraphs = utils.combiner(paragraphs)

            #print("after combining---------------")
            #print(paragraphs)
            
            # 2. Clean up step 1, remove quatations & slice the content into paras
            
            para_list = utils.preprocess0(paragraphs)

            #3.Break down into sentences
            content_df.at[para_i,'sentences'] = ''
            for para in para_list:
                #print(".....")

                para = utils.preprocess2(para)
                #print(para)

                sent_list = utils.sentencer(para)

                #content_df['sentences'] = content_df['sentences'].astype('object') 
                
                content_df.at[para_i,'sentences']  = content_df.at[para_i,'sentences'] +  ''.join(sent_list) 

                #print(sent_list)

            para_i = para_i + 1

        #print(content_df.head())

        orginal_file_name = os.path.basename(file)

        op_file = './op/' + "parsed_" + orginal_file_name

        # write parsed sentences for each article
        content_df.loc[:,['UUID','sentences']].to_csv(op_file,index=False)

        print("Parsed content stored in ", op_file)

    
    
    