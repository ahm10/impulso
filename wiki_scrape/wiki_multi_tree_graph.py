import spacy
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import glob
import itertools
nlp_blank = spacy.blank('en')
from spacy.matcher import PhraseMatcher


### name of topics to be constructed tree for (would be replaced with unique tags sets later) 

topics = ['Machine_learning','Supervised_learning','Regression_analysis']

t = 0

entity_pairs_list = []
relations_list = []

#### Get the hierarchy first

combined_df = pd.DataFrame(columns=['parent','child','color'])

for filename in glob.glob('./scrapped_data/*.json'): 

    topic = topics[t]
    print("\n---",topic,"---") 
    print("constructing tree....")

    t = t + 1 


    with open(filename) as f:
        scrapped_data = json.load(f)

    sections = scrapped_data['sections']

    df = pd.DataFrame(columns=['level','heading'])

    graph_df=pd.DataFrame(columns=['child','parent'])
    
    for section in sections:

        for k,v in section.items():

            df = df.append({'level': k, 'heading' : v},ignore_index=True)


    index = df.index
    level1_index = list(df[df['level']=='1'].index)
    level2_index = list(df[df['level']=='2'].index)
    level3_index = list(df[df['level']=='3'].index)
    
    # print(level1_index)
    # print(level2_index)
    # print(level3_index)
    # print(index)

    k = 0

    # level 0 - level1 child parent relations

    for l1 in level1_index:
        graph_df.loc[k,'child'] = df.loc[l1,'heading']
        graph_df.loc[k,'parent'] = topic # the base topic
        graph_df.loc[k,'color'] = 'red'
        k = k + 1

    # define edge colors for level 0-1
    

    # leve1 - level2 child parent relations

    level1_p = list(zip(level1_index, level1_index[1:])) 

    #print(level1_p)
    for (l1_start,l1_end) in level1_p:
        # print((l1_start,l1_end))
        if(l1_end - l1_start > 1): 

            # print("found parent", df.loc[l1_start,'heading'])

            for l2 in range(l1_start+1,l1_end,1):

                if(l2 in level2_index):

                    newchild = df.loc[l2,'heading']

                    if (newchild not in graph_df['child']): 
                        graph_df.loc[k,'child'] = df.loc[l2,'heading']
                        graph_df.loc[k,'parent'] = df.loc[l1_start,'heading']
                        graph_df.loc[k,'color'] = 'blue'
                        k = k + 1

    # leve2 - level3 child parent relations

    level2_p = list(zip(level2_index, level2_index[1:])) 

    #print(level2_p)
    for (l2_start,l2_end) in level2_p:
        # print((l2_start,l2_end))
        if(l2_end - l2_start > 1): 

            # print("found parent", df.loc[l2_start,'heading'])

            for l3 in range(l2_start+1,l2_end,1):

                if(l3 in level3_index):

                    newchild = df.loc[l3,'heading']

                    if (newchild not in graph_df['child']): 
                        graph_df.loc[k,'child'] = df.loc[l3,'heading']
                        graph_df.loc[k,'parent'] = df.loc[l2_start,'heading']
                        graph_df.loc[k,'color'] = 'green'
                        k = k + 1


    print("> No. of nodes added...",k)
    # save each topic tree file for structured data folder
    #graph_df.to_csv("./structured_data/"+topic+"_tree.csv")


    # make a combined data file 

    combined_df = combined_df.append(graph_df)
    
    #print("....",combined_df.head())


    # create a directed-graph from one topic dataframe
    
    # G = nx.from_pandas_edgelist(graph_df, source='parent',target='child')
    # plt.figure(figsize=(12,12))

    # pos = nx.spring_layout(G)
    # nx.draw(G, with_labels=True, edge_color=graph_df['color'])
    # #plt.show()
    # plt.savefig('./figures/' + topic + '_knowledge_graph.png')




### store combined data




combined_data_file = "./structured_data/"+"combined_tree.csv"
combined_df.to_csv(combined_data_file)

print("\n----------------------------")

print("Total No.of topics added..",t)
print("Total no of nodes..", len(combined_df))
print("Combined data tree written at ",combined_data_file)
### combined graph 

G1 = nx.from_pandas_edgelist(combined_df, source='parent',target='child')
plt.figure(figsize=(12,12))
pos = nx.spring_layout(G1)
nx.draw(G1, with_labels=True, edge_color=combined_df['color'])
#plt.show()
plt.savefig('./figures/' + 'combined' + '_knowledge_graph.png')