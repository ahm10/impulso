from langdetect import detect
import re

import spacy
from spacy_langdetect import LanguageDetector
nlp = spacy.load('en')

def check_charecters(txt):

       return all(ord(c) < 128 for c in txt)
        

def check_lang(txt):
    txt = str(txt) + ' '
    # create a pipe if not already created 
    if "language_detector" not in nlp.pipe_names:
        nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

    doc = nlp(txt)
# document level language detection. Think of it like average language of the document!
    if(doc._.language['language']=='en'):
        return txt
    else:
        return ''
 

def preprocess0(tag_list):

    start = '['
    end = ']'

    tags = []
    # remove brackets from the string
    if (start in tag_list and end in tag_list): # a valid list

        tag_contents = tag_list.split(start)[1].split(end)[0]

        tags = tag_contents.split(',')

    return tags

def combiner(paragraphs):

    '''
     Combine the steps or subtopic explanations with : or -
     Join the numbered bullet points into one para
    '''

    paragraphs = re.sub(r":\s*',\s*'", ": ",paragraphs) 

    paragraphs = re.sub(r"-\s*',\s*'", ": ",paragraphs) 

    # combine numbered lists in one para

    paragraphs = re.sub(r"'\s*,\s*'\d.\s*", " \u2022 ",paragraphs) 

    # combine unnumbered lists in one para

    paragraphs = re.sub(r"'\s*,\s*'\u2022.\s*", " \u2022 ",paragraphs) 


    return paragraphs

def preprocess1(tags):
            tags = tags.replace("'", "")
            tags = tags.replace("'","")
            tags = tags.rstrip(" ")
            tags = tags.lstrip(" ")
            # remove special charecters    
            tags = re.sub('[^A-Za-z0-9]+', ' ', tags)

            return tags

def preprocess2(txt):
            txt = txt.lstrip(" ")
            txt = txt.lstrip("'")
            txt = txt.rstrip("'")
            # remove special charecters    
            #txt = re.sub('[^A-Za-z0-9]+', ' ', txt)

            return txt

      
def sentencer(txt): 
    '''
    split each sentence into singular part

    '''
    sent_list = [txt]

    

    if ('.' in txt):

        sent_list = txt.split('.')

        # make provision to ignore decimal points as periods
        #txt = re.split(r'\.(?<!\d)\.(?!\d)',txt)


    return sent_list[:-1]



