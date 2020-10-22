import spacy
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
nlp_blank = spacy.blank('en')
from spacy.matcher import PhraseMatcher

theme_list = ['machine learning']
algorithms_list = ['artificial intelligence']
matcher = PhraseMatcher(nlp_blank.vocab)
matcher.add('theme', None, *[nlp_blank(entity_i) for entity_i in theme_list])


doc = nlp_blank("ML is short of machine learning. Machine learning is advance field.")
matches = matcher(doc)

for m_id, start, end in matches:
    entity = doc[start : end] 
    print((entity.text, entity.start_char, entity.end_char, nlp_blank.vocab.strings[m_id]))


##################### hand pick

filename = './parsed_data/' + "parsed_wiki_content_Machine learning.json"

with open(filename) as f:
  parsed_data = json.load(f)

print(len(parsed_data))

entity_pairs = [['','']] * (len(parsed_data) + 1)

relations = [''] * (len(parsed_data) + 1)

entity_pairs[0] = ['artificial intelligence', 'machine learning']

relations[0] = 'issubset'

entity_pair = ['machine learning','']
i = 1
for heading in parsed_data.keys():

    print("heading-",heading)

    #entity_pair[1] = heading
    entity_pairs[i] = ['machine learning',heading]
    relations[i] = 'contains'
    i = i + 1
    
print(entity_pairs)

print(relations)

#entity_pairs = [['artificial intelligence', 'machine learning'],['machine learning','Definition'],['machine learning','Overview'],['machine learning','Machine learning approaches'],['machine learning','History and relationships to other fields']]




# extract subject
source = [i[0] for i in entity_pairs]

# extract object
target = [i[1] for i in entity_pairs]



kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

# create a directed-graph from a dataframe
G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(12,12))

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
#plt.show()
plt.savefig('machine_learning_Example_knowledge_graph.png')
