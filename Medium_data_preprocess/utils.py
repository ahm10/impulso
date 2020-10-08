import re

def preprocess0(tag_list):

    start = '['
    end = ']'

    tags = []
    # remove brackets
    if (start in tag_list and end in tag_list): # a valid list

        tag_contents = tag_list.split(start)[1].split(end)[0]

        tags = tag_contents.split(',')

    return tags



def preprocess1(txt):
            txt = txt.replace("'", "")
            txt = txt.replace("'","")
            txt = txt.rstrip(" ")
            txt = txt.lstrip(" ")
            # remove special charecters    
            txt = re.sub('[^A-Za-z0-9]+', ' ', txt)

            return txt