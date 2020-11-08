from grakn.client import GraknClient
import csv
import pandas as pd
import json
import os
import grakn_utils



######### DATA COLLECTION
parsed_path = "../../wiki_scrape/parsed_data/"
parsed_files = os.listdir(parsed_path)

 
for filename in parsed_files:
    print("Collecting data from...",filename)
    topic_to_do = filename.split("parsed_")[1].split(".json")[0]
    # topic_to_do = "Machine_learning"

 
    ## get conts for topics 

    with open(parsed_path + "parsed_" + topic_to_do +".json") as f:
        cont = json.load(f)
        cont_keys = cont.keys()

    ## get the tree structure for indexing

    print("---DATA COLLECTION FOR " + topic_to_do + " ------")
    cols = ['child','parent','rel_level']
    structured_path = "../../wiki_scrape/structured_data/"
    tree_structure = pd.read_csv(structured_path + topic_to_do +"_tree.csv")
    

    topic_seq = ['topic','subtopic1','subtopic2','subtopic3']
    re_seq = ['rel1','rel2','rel3']     

    n = len(tree_structure)

    keys = topic_seq + re_seq
    # print(keys)
    D = dict(zip(keys,[]))

    for key in keys:
        D[key] = []

    # print(D)

    # organize each item 
    for k in range(n):

        rel_level = tree_structure.loc[k,'rel_level'] 

        child_type = topic_seq[rel_level]

        parent_type = topic_seq[rel_level -1 ]
        
        new_child = tree_structure.loc[k,'child']
        if (grakn_utils.check_entered(new_child,D[child_type]) and new_child in cont_keys): # if not added already

            D[child_type].append({"title":new_child, "txt" : cont[new_child]})


        new_parent = tree_structure.loc[k,'parent']
        if (grakn_utils.check_entered(new_parent,D[parent_type])):    

            if (new_parent == topic_to_do): # base level to be set with intro text
                cont_key = 'introduction'
            D[parent_type].append({"title" : new_parent, "txt" : cont[cont_key]})

        rel_type = re_seq[rel_level -1]

        new_rel = {child_type: new_child,parent_type: new_parent}

        D[rel_type].append(new_rel)
        

    # print(D)
 

    # create inputs 
    inputs = grakn_utils.create_inputs()

    # Build the graph (refer grakn utils to understand the entire flow)
    grakn_utils.build_zeitlabs_graph(inputs=inputs,D=D)