from grakn.client import GraknClient
# from fuzzywuzzy import fuzz

import pandas as pd

filters = ["See also", "References", "Journals", "External links", "Further reading", "Conferences"]

dont_know = "\nI am afraid I dont know much about it. \n Would you like to rephrase your question?"

Tparents_list = []

Tchild_list = []

def describe1(topic_val): 

    desc = "the description of " + topic_val
    return desc


def query_grakn(q): 
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "impulso2") as session:
            with session.transaction().read() as transaction:
 

                q = "".join(qq for qq in q)

                iterator = transaction.query(q)
                answers = [ans.get("x") for ans in iterator]
                result = [ answer.value() for answer in answers ]

                return result


def describe(test_topic): 


    desc = "Exploring...\n "


    ### query to fetch intro

    test_subtopic = "introduction"

    q_intro = [
            'match',
            '  $t1 isa Tparent, has title "' + test_topic + '";',
            '  $t2 isa Tchild, has title "' + test_subtopic + '";'
            '  (parent: $t1, child: $t2) isa ConsistsOf, has content $x;',
            'get $x;'
        ]


    results_intro = query_grakn(q_intro)

    intro = ''

    if (len(results_intro)): 

        intro = results_intro[0]

 
    desc = desc + intro + "\n"


    ### query to fetch subtopics

    q = [
        'match',
        '  $t1 isa Tparent, has title "' + test_topic + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;'
    ]


    result = query_grakn(q)

    if(len(result)):

        result_str = process_result_bullets(result) 

        msg = "On this topic, I can also tell you about " + "\n" + result_str

    else: 
        msg = dont_know 
    
    desc = desc + msg

    return desc


def describe2(test_topic,test_subtopic): 


    desc = "Searching...\n "


    ### query to fetch subtopic content

 
    q = [
            'match',
            '  $t1 isa Tparent, has title "' + test_topic + '";',
            '  $t2 isa Tchild, has title "' + test_subtopic + '";'
            '  (parent: $t1, child: $t2) isa ConsistsOf, has content $x;',
            'get $x;'
        ]

    results = query_grakn(q)

    if(len(results)):

        result_str = str(results[0]) 

        msg = test_subtopic + ":\n" + result_str

        ## also check for inner topics

        q1 = [
        'match',
        '  $t1 isa Tparent, has title "' + test_subtopic + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;']

        result1 = query_grakn(q1)


        if(len(result1)):

            result_str1 = process_result_bullets(result1) 

            msg = msg + "\n" + result_str1


    else: 
        msg = dont_know 
    
    desc = desc + msg 

    return desc

def get_Tparent_list(): 

    q = [
        'match',
        '  $t1 isa Tparent, has title $x;',
        'get $x;'
    ]

    result = query_grakn(q)

    return result


def get_Tchild_list(test_topic): 


    q = [
        'match',
        '  $t1 isa Tparent, has title "' + test_topic + '";',
        '  $t2 isa Tchild, has title $x;'
        '  (parent: $t1, child: $t2) isa ConsistsOf;',
        'get $x;'
    ]

    result = query_grakn(q)

    return result


def process_Tparent_name(topic): ## to be edited

    t = topic.lower()
    
    Tparent_list = get_Tparent_list()

    r = dict()

    r['grakn'] = topic

    r['user'] = topic

    # r = str(len(Tparent_list))

    for e in Tparent_list:

        e1 = e.replace('_', " ").lower()

        # Ratio = fuzz.ratio(e1.lower(),t.lower())

        # if (Ratio > 60): 
        #     r['grakn'] = e

        #     r['user'] = e1

        #     break

        # Partial_Ratio = fuzz.partial_ratio(e1.lower(),t.lower())

        # if (Ratio > 50 and Partial_Ratio > 50):

        ################

        start = t.find(e1)

        if (start > -1): 

            r['grakn'] = e # original topic name from grakn

            r['user'] = e1

            break


    return r


def process_Tchild_name(Tparent,Tchild): ## to be edited

    
    Tchild_list = get_Tchild_list(Tparent)

    r = dict()

    r['grakn'] = Tchild

    r['user'] = Tchild

    # r = str(len(Tparent_list))

    for e in Tchild_list:


        e1 = e.replace('_', " ").lower()

        # Ratio = fuzz.ratio(e1.lower(),t.lower())

        # Partial_Ratio = fuzz.partial_ratio(e1.lower(),t.lower())

        # if (Ratio > 50 and Partial_Ratio > 50):

        start = Tchild.find(e1)

        if (start > -1): 

            r['grakn'] = e # original topic name from grakn

            r['user'] = e1

            break


    return r

def process_result_bullets(list):


    # get bullets 

    bullet = "- "
    
    bulleted_list = [bullet + item for item in list if item not in filters] 


    list_str = ',\n'.join([str(elem) for elem in bulleted_list if elem not in filters]) 

    list_str = list_str.replace("_", " ")

    return list_str



