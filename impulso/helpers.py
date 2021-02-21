from grakn.client import GraknClient
# from fuzzywuzzy import fuzz

import pandas as pd

import grakn_utils

import random

import re

additional = ["see_also", "references", "journals", "external_links", "further_reading", "conferences"]

dont_know = "\nI am afraid I dont know much about it. \n Would you like to rephrase your question?"

Tparents_list = []

Tchild_list = []

def continue_q(topic): 
    
    cq1 = "\n\n Would you like to continue discussing " + topic + " (yes/no)?"
    cq2 = "\n\n Should we continue on " + topic + " (yes/no)?"
    cq3 = "\n\n Would you like to know more on " + topic + " (yes/no)?"
    cq4 = "\n\n Shall we continue exploring " + topic + " (yes/no)?"

    continueq = [cq1,cq2,cq3,cq4]

    random.shuffle(continueq)

    return continueq[0]


def reset_msg(): 

    rq1 = "\n Or we can always make a fresh start! Just say restart!"
    rq2 = "\n Or Here are some shortcuts [stop, restart, change topic]"
    rq3 = "\n Or Would you like to try another topic? change is the word!"
    rq4 = "\n Want to explore a new topic? change is the word!"

    rq = [rq1,rq2,rq3,rq4]

    random.shuffle(rq)

    return rq[0]

def dontknow(): 
    dq1 = "\n I am afraid I dont understand. Would you perhaps repharse the question?"
    dq2 = "\n I am sorry I am not clear on what you are asking. Would you perhaps repharse the question?"
    dq3 = "\n Oops, I think I am confused, would you like pose another question?"
    dq4 = "\n Oops, I have trouble understanding this. Can you please trying posing a simpler question?"

    dq = [dq1,dq2,dq3,dq4]

    random.shuffle(dq)

    rq = reset_msg()



    return dq[0] + rq


def process_topic_names(topicname):
    return topicname.replace(' ','_').lower().replace('"','`').replace("'","`")

def reverse_process_topic_names(topicname):
    return topicname.replace('_',' ').lower().replace('"','`').replace("'","`").replace("(", " ").replace(')'," ").replace('-',' ')

def get_topicID(current_topic,current_level):

    ## level based query to be done later 

    id = ''

    if (current_level=='1'): 

        current_topic = process_topic_names(current_topic)

        q = [
        'match',
        '  $t1 isa Tparent, has title "' + current_topic + '", has UUID $x;',
        'get $x;'
    ]

        q = "".join(q)

        result = query_grakn(q)

        if (len(result)): 
            id = result[0]

    return id 


def describe(topic_val): 

    desc = "the description of " + topic_val
    return desc


def query_grakn(q): 
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "impulso0") as session:
            with session.transaction().read() as transaction:
 

                q = "".join(qq for qq in q)

                iterator = transaction.query(q)
                answers = [ans.get("x") for ans in iterator]
                result = [ answer.value() for answer in answers ]

                return result




def describe_wiki_Tparent(current_topic,current_level,topic_turn_w,intent): 


    desc = ">>\n" 


    ### query to fetch intro

    if (topic_turn_w==0): 
        subtopic = "introduction"

        q_intro = [
                'match',
                '  $t1 isa Tparent, has title "' + current_topic + '", has path_depth "' + current_level + '";',
                '  $t2 isa Tchild, has title "' + subtopic + '";'
                '  (parent: $t1, child: $t2) isa ConsistsOf, has content $x;',
                'get $x;'
            ]


        q_intro = "".join(q_intro)
        # desc += q_intro



        results_intro = query_grakn(q_intro)

        intro = ''

        if (len(results_intro)): 

            intro = results_intro[0]

    
        desc = desc + intro + "\n"

    elif topic_turn_w > 0:
    ### query to fetch subtopics

        q = [
            'match',
            '  $t1 isa Tparent, has title "' + current_topic + '", has path_depth "' + current_level + '";',
            '  $t2 isa Tchild, has title $x;'
            '  (parent: $t1, child: $t2) isa ConsistsOf;',
            'get $x;'
        ]

        q = "".join(q)

        result = query_grakn(q)

        msg = ''

        if(len(result)):

            result_str = process_result_bullets(result) 

            msg = "On this topic, I can also tell you about " + "\n" + result_str 

        else: 
            msg = dont_know 
        
        desc = desc + msg

    return desc



def describe_research(topic_UUID,Tchild_grakn,current_level,topic_turn_r,topic_turn_w,content_type,intent): 

    # default 
    msg = dont_know

    if (current_level=='1'): 

        desc = ">>\n "


        n_articles = 1





############ get title
        q = [
                    'match',
                    '  $t1 isa Tparent, has UUID "' + topic_UUID + '";',
                    '  $t2 isa article, has title $x;'
                    '  (parent: $t1, supplement: $t2) isa ExplainedIn, has content $c;',
                    'get $x;'
                    ]

        q = "".join(q)
        result1 = query_grakn(q)

######### get url
        q = [
                    'match',
                    '  $t1 isa Tparent, has UUID "' + topic_UUID + '";',
                    '  $t2 isa article, has URL $x;'
                    '  (parent: $t1, supplement: $t2) isa ExplainedIn, has content $c;',
                    'get $x;']

        q = "".join(q)
        result2 = query_grakn(q)


        result = [x + " [link : "+ y.split('?')[0] + "]" for x,y in zip(result1,result2)]

        ## shuffle it
        random.shuffle(result)

        if(len(result)):

            result_str = process_result_bullets(result[:n_articles]) 

            a = ["Here is an interesting article, ", " An interesting read for you-", " You might like this too.."]

            random.shuffle(a)

            msg = a[0] + "\n" + result_str 

            

        else: 
            msg = dont_know 
        
        desc = desc + msg

    return desc



def describe_wiki_Tchild(parent_topic,current_topic,current_level,topic_turn_r,topic_turn_w,content_type,intent): 


    desc = ">>\n "


    ### query to fetch subtopic content

 
    q = [
            'match',
            '  $t1 isa Tparent, has title "' + parent_topic + '";',
            '  $t2 isa Tchild, has title "' + current_topic + '", has path_depth "' + str(current_level) + '";'
            '  (parent: $t1, child: $t2) isa ConsistsOf, has content $x;',
            'get $x;'
        ]

    q = "".join(q)

    results = query_grakn(q)

    # desc += q
    msg = "" 
    if(len(results)):

        result_str = str(results[0]) 

        msg = reverse_process_topic_names(current_topic) + ":\n" + result_str

        ## also check for inner topics

        # send current topic as parent
        child_list = get_Tchild_list(parent_topic,current_topic,current_level)


        if(len(child_list)):

            result_str1 = process_result_bullets(child_list) 

            msg = msg + "\n" + result_str1


    # else: 

    #     # find a back up answer on parent topic
    #     parentID = get_topicID(parent_topic)
        
    #     research_msg = describe_research(parentID,'1')

    #     msg = research_msg 
    
    desc = desc + msg 

    return desc

def welcome_topic_list(): 

    q = [
        'match',
        '  $t1 isa Tparent, has title $x, has path_depth "' + str(1) + '";',
        'get $x;'
    ]

    result = query_grakn(q)

    return result

def get_Tparent_list(current_topic,current_level):

    return None

def get_valid_Tchild_list(parent_topic,current_topic,level): 


    # q = [
    #     'match',
    #     '  $t1 isa Tparent, has title "' + test_topic + '";',
    #     '  $t2 isa Tchild, has title $x;'
    #     '  (parent: $t1, child: $t2) isa ConsistsOf;',
    #     'get $x;'
    # ]
    

    q = [
        'match',
        '  $t1 isa Tparent, has title "' + parent_topic + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;'
    ]
    result = query_grakn(q)

    return result



def get_adjacents(parent_topic,current_topic,current_level): 


    # q = [
    #     'match',
    #     '  $t1 isa Tparent, has title "' + test_topic + '";',
    #     '  $t2 isa Tchild, has title $x;'
    #     '  (parent: $t1, child: $t2) isa ConsistsOf;',
    #     'get $x;'
    # ]
    

    q = [
        'match',
        '  $t1 isa Tparent, has title "' + parent_topic + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;'
    ]

    q = "".join(q)
    result = query_grakn(q)

    # remove already seen child

    if (current_topic in result): 
        result.remove(current_topic)


    result = process_result_bullets(result)

    return result

def get_Tchild_list(parent_topic,current_topic,current_level): 


    # q = [
    #     'match',
    #     '  $t1 isa Tparent, has title "' + test_topic + '";',
    #     '  $t2 isa Tchild, has title $x;'
    #     '  (parent: $t1, child: $t2) isa ConsistsOf;',
    #     'get $x;'
    # ]
    

    q = [
        'match',
        '  $t1 isa Tparent, has title "' + current_topic + '", has path_depth "' + current_level + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;'
    ]

    q = "".join(q)
    result = query_grakn(q)


    return result


def validate_Tparent_name(topic,current_level): ## to be edited

    t = process_topic_names(topic)

    if current_level=='1':
        Tparent_list =welcome_topic_list()

    #else: 
    # Tparent_list = get_Tparent_list(topic,current_level)

    r = dict()

    r['grakn'] = topic

    r['user'] = topic

    # r = str(len(Tparent_list))

    for e in Tparent_list:

        e1 = e.replace('_', " ").lower()

        start = t.find(e1)

        if (start > -1): 

            r['grakn'] = e # original topic name from grakn

            r['user'] = e1

            break


    return r

    

def validate_Tchild_name(parent_topic,current_topic,current_level): ## to be edited
    
    Tchild_list = get_valid_Tchild_list(parent_topic,current_topic,current_level)
    r = dict()
    r['grakn'] = current_topic
    r['user'] = current_topic

    current_topic = "".join(current_topic)

    current_topic = current_topic.replace('?','')

    current_topic_tokens = current_topic.split(" ")

    # clean current_topic_tokens

    current_topic_tokens = [re.sub('[^A-Za-z0-9 ]+', '', c) for c in current_topic_tokens]

    for child in Tchild_list: 

        child_simple = reverse_process_topic_names(child)

        child_simple_tokens = child_simple.split(" ")

        for child_token in child_simple_tokens:

            if child_token in current_topic_tokens: # found any word match
                r['grakn'] = child # this is the node 
                r['user'] = reverse_process_topic_names(child)

 
    return r

def process_result_bullets(list):


    # get bullets 

    bullet = "- "
    
    bulleted_list = [bullet + item for item in list if item not in additional] 


    list_str = ',\n'.join([str(elem) for elem in bulleted_list if elem not in additional]) 

    list_str = list_str.replace("_", " ")

    return list_str



