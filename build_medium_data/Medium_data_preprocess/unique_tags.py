''''

The script parses the output content of medium text scrapping module.
It produces list of unique tags along with total number of occurances of each tag.
The occurance can be used to decide the priority of the tag.

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import utils
import numpy as np
# raw_data = pd.read_csv('contents_op_data_engineering_5000.csv')

# collect all content files placed in data folder
scraped_files = glob.glob('data/*.csv')

frames =[]

# read each file one by one
for file in scraped_files:
    #all of the scraped data from different tags
    df = pd.read_csv(file)
    frames.append(df) # append data from each file into a dataframe

raw_data = pd.concat(frames) #combine all frames into one
# raw_data.head()
 
# Get lists of tags

tags_lists = raw_data['tags']
#print("tags_list:",tags_lists)

# set counters

total_tags = 0

#set empty data dict
unique_tags_occurance = {}

# go through each list 

entire_list = []

for tag_list in tags_lists:


        # split on comma to get all tags as individual elements

        tags = utils.preprocess0(tag_list)

        #print(len(tags))
        


        #print("tags",len(tags))

        for tag in tags: # preprocess and check each tag
            #print(tag)
            total_tags = total_tags + 1
            # preprocess

            tag = utils.preprocess1(tag)

            entire_list.append(tag)

            if tag not in unique_tags_occurance.keys(): # record the tag if not already there
                unique_tags_occurance[tag] = 0
            elif tag in unique_tags_occurance.keys(): # count the occurance if it appears again
                unique_tags_occurance[tag] += 1
 

 
print( "\n >> total tags processed = ", total_tags, ". Unique tags = ",len(unique_tags_occurance))



# sort tags on occurance

sorted_unique_tags_occurance = {k: v for k, v in sorted(unique_tags_occurance.items(), key=lambda item: item[1],reverse=True)}

#print(sorted_unique_tags_occurance)

unique_tags_df = pd.DataFrame(columns = ['tag','occurance'])

unique_tags_df.tag = sorted_unique_tags_occurance.keys()

unique_tags_df.occurance = sorted_unique_tags_occurance.values()


print("\n\n -----------------Top 5 tags:------------------")



print(unique_tags_df.head())



op_file = './op/unique_tags_occurance.csv'

unique_tags_df.to_csv(op_file,index=False)

print("unique tags occurance stored in ", op_file)



 