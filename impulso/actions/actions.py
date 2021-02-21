# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

import helpers as h1 

import random

additional = ["see_also", "references", "journals", "further_reading", "conferences"]

reseach_types = ['reserch','research','happening','article','articles','trends','trend','update','updates','new', 'news','example','examples','application','applications','innovation','innovations']
class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                    
        Tparent_list = h1.welcome_topic_list()


        desc = ''
        # desc = "Hi! my name is Impulso. I am your learning assistant."
        desc = "\n Here are few topics we can talk about!\n"

        n = 5

        random_Tparent_list_samples = random.sample(Tparent_list, n)

        msg = h1.process_result_bullets(random_Tparent_list_samples)

        desc = desc + msg

        desc = desc + "\n Which topic would you like to discuss?"
        dispatcher.utter_message(text=desc)

        return [SlotSet("topic_turn_r", 0),SlotSet("topic_turn_w", 0),SlotSet("content_type", "wiki"),SlotSet("Tparent_store", None), SlotSet("Tparent", None),SlotSet("Tchild_store", None), SlotSet("Tchild", None),SlotSet("current_level", None)]


class ActionReset(Action):

    def name(self) -> Text:
        return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            

        dispatcher.utter_message(text="Reset successful. Say Hi to initiate a conversation!")

        return [SlotSet("topic_turn_r", 0),SlotSet("topic_turn_w", 0),SlotSet("Tparent_store", None), SlotSet("Tparent", None),SlotSet("Tchild_store", None), SlotSet("Tchild", None),SlotSet("current_level", None)]



class ActionS(Action):

    def name(self) -> Text:
        return "action_s"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            

        dispatcher.utter_message(text="jsn!")

        return [SlotSet("content_type", None), SlotSet("TparentID", None),SlotSet("current_level", None),SlotSet("Tparent_store", None), SlotSet("Tparent", None)]


class ActionS1(FormAction):

    def name(self) -> Text:
        return "action_s1"

    @staticmethod

    def required_slots(tracker):

        req_slots = ["Tparent"]

        return req_slots

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        desc = ''

        current_level = str(1)   
            
        Tparent_val = tracker.get_slot("Tparent")

        content_type = tracker.get_slot("content_type")

        topic_turn_w = tracker.get_slot("topic_turn_w")

        topic_turn_r = tracker.get_slot("topic_turn_r")

        intent = ''

        intent = tracker.latest_message['intent'].get('name')


        if (not topic_turn_w): 
            topic_turn_w = 0
        
        if (not topic_turn_r): 
            topic_turn_r = 0

        # # process the user input value

        # # Tparent_vals = h1.validate_Tparent_name(Tparent_val,current_level)

        # # Tparent_grakn = Tparent_vals['grakn']

        # # Tparent_user = Tparent_vals['user']

        # desc = h1.dontknow() # default

        Tparent_grakn = h1.process_topic_names(Tparent_val)

        desc += Tparent_val

        TparentID = h1.get_topicID(Tparent_grakn,current_level)


        # desc = h1.describe_wiki_Tparent(Tparent_grakn,current_level)
     
        if (content_type in reseach_types):

            if (len(TparentID)):  # send with empty child as it is not reqd
                desc = h1.describe_research(TparentID,'',current_level,topic_turn_r,topic_turn_w,content_type,intent)

            # increment content type turn on the topic
            topic_turn_r = topic_turn_r + 1
 
        else: # wiki case

            content_type = 'wiki'
            desc += Tparent_grakn + current_level
            
            desc = h1.describe_wiki_Tparent(Tparent_grakn,current_level,topic_turn_w,intent)

            if (len(desc) < 3): 
                desc = "\n I am not sure if I got the topic name, can you please check for typos or rephrase? (If stuck, You can always reset to start over)"

            else:
                desc = desc +  "Would you like to continue on " + Tparent_val + "(yes/no)?"
                topic_turn_w = topic_turn_w + 1

        dispatcher.utter_message(text=desc)


        #     # switch it back to wiki by default
            # content_type = "wiki"
            
        
        
        # dispatcher.utter_message(text=desc)

        return [SlotSet("topic_turn_r", topic_turn_r),SlotSet("topic_turn_w", topic_turn_w),SlotSet("content_type", content_type), SlotSet("TparentID", TparentID),SlotSet("current_level", current_level),SlotSet("Tparent_store", Tparent_grakn), SlotSet("Tparent",Tparent_val )]


class ActionS2(FormAction):

    def name(self) -> Text:
        return "action_s2"

    @staticmethod

    def required_slots(tracker):

        req_slots = ["Tchild"]

        return req_slots    

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        desc = ''

        current_level = tracker.get_slot("current_level")

        current_level = str(current_level)

        if not current_level: 
            current_level = '1'
        
        new_level = current_level

        Tparent_user = tracker.get_slot("Tparent")

        Tparent_grakn = tracker.get_slot("Tparent_store")

        Tchild_user = tracker.get_slot("Tchild")

        Tchild_grakn = Tchild_user # place holder value

        article = tracker.get_slot("article")


        # Tchild_grakn = h1.process_topic_names(Tchild_user)

        topic_turn_w = tracker.get_slot("topic_turn_w")

        topic_turn_r = tracker.get_slot("topic_turn_r")

        content_type = tracker.get_slot("content_type")

        TparentID = tracker.get_slot("TparentID")

        intent = tracker.latest_message['intent'].get('name')



        if content_type not in reseach_types: # look in wiki

            # increase wiki counter 
            # desc += "in=" + Tchild_grakn
            Tchild_grakn = h1.validate_Tchild_name(Tparent_grakn,Tchild_user,current_level)['grakn']

            Tchild_user = h1.validate_Tchild_name(Tparent_grakn,Tchild_user,current_level)['user']

            # desc += "out=" + Tchild_grakn
            topic_turn_w = topic_turn_w + 1

            # desc = h1.dontknow() # default

            # desc = 'looking for ' + Tchild_grakn


            if (Tparent_grakn and Tchild_grakn): 

                # Tchild_vals = h1.validate_Tchild_name(Tparent_grakn,Tchild_val,asked_level)

                # Tchild_grakn = Tchild_vals['grakn']

                # Tchild_user = Tchild_vals['user']

                desc = h1.describe_wiki_Tchild(Tparent_grakn,Tchild_grakn,current_level,topic_turn_r,topic_turn_w,content_type,intent)

            #### if no match found in wiki, give list of sub topics
                if (len(desc) < 3): 

                    desc += "I am afraid I am not able to understand what you are looking for.\n"

                    desc+= h1.describe_wiki_Tparent(Tparent_grakn,current_level,topic_turn_w,intent)
                    # get list of children

                    # desc = h1.describe_research(TparentID,Tchild_grakn,'1',topic_turn_r,topic_turn_w,content_type,intent)
                    # topic_turn_r = topic_turn_r + 1
                    # content_type = 'research'
                    # set article entity

                else: # successful find in wiki
                    new_level = str(int(new_level) + 1)
                    topic_turn_w = topic_turn_w + 1
                    

        
        else: 

                        # increase med counter
            topic_turn_r = topic_turn_r + 1

            desc = h1.describe_research(TparentID, Tchild_grakn , '1',topic_turn_r,topic_turn_w,content_type,intent)
            # set article entity

            if (len(desc) > 3 and '-' in desc and '[' in desc):
                article = desc.split('[')[0].split('-')[1].lstrip().rstrip()
 
        # strip down extra response

        desc = desc.split(']')[0]

        # ask for continuation
        cq1 = "\n" + Tparent_user + " seems to be interesting for you! isn't it?"
        cq2 = "\n Shall I go on exploring on "+ Tparent_user + "? yes/no"
        cq3 = "\n Would you want me to go on with "+ Tparent_user + "? or you want to try another topic?"
        cq4 = "\n Are we on right path exploring " + Tparent_user + "? or you are bored of this topic? :) pls if I should continue.."
        cq = [cq1,cq2,cq3,cq4]

        random.shuffle(cq)
        desc+= cq[0]

        dispatcher.utter_message(text=desc)

        ## clear child for new instance

        return [SlotSet("article", article),SlotSet("topic_turn_r", topic_turn_r),SlotSet("topic_turn_w", topic_turn_w),SlotSet("content_type", content_type), SlotSet("TparentID", TparentID),SlotSet("current_level", new_level),SlotSet("Tchild_store", Tchild_grakn), SlotSet("Tchild", Tchild_user)]




class ActionS4(Action):

    def name(self) -> Text:
        return "offer_options"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        desc = ''

        current_level = tracker.get_slot("current_level")

        current_level = str(current_level)

        if not current_level: 
            current_level = '1'
        else:
            new_level = int(current_level) + 1

        Tparent_user = tracker.get_slot("Tparent")

        Tparent_grakn = tracker.get_slot("Tparent_store")

        Tchild_user = tracker.get_slot("Tchild")

        Tchild_grakn = tracker.get_slot("Tchild_store")

        article = tracker.get_slot("article")

        topic_turn_w = tracker.get_slot("topic_turn_w")

        topic_turn_r = tracker.get_slot("topic_turn_r")

        content_type = tracker.get_slot("content_type")

        TparentID = tracker.get_slot("TparentID")

        intent = tracker.latest_message['intent'].get('name')

        # find similar articles/wiki in case of next level

        if (intent=='next_level_affirm'):

            if (content_type=='wiki'): 


                desc = ''


                # try to get children or siblings ----------


                if (Tparent_grakn and Tchild_grakn):
                    res_child = h1.get_Tchild_list(Tparent_grakn,Tchild_grakn,current_level)
                elif (len(Tparent_grakn)): 
                    res_child = h1.get_Tchild_list('',Tparent_grakn,current_level)


                found_sib = 0
                found_child = 0
                desc_temp = dict()
                if (len(res_child) > 3): 

                    tc = ''

                    if (Tchild_user):
                        tc = " on " + Tchild_user 
                    
                    res_child = h1.process_result_bullets(res_child)
                    desc_temp['c'] = "In " + Tparent_user + tc +  ", You can also learn about,\n" + res_child 

                    found_child = 1
            

                # get neighbours
                                          #parent_topic,current_topic,current_level
        
                res_sib= h1.get_adjacents(Tparent_grakn,Tchild_grakn,current_level)


                if(len(res_sib) > 3): # found adj
                    
                    tc = ''
                    if (Tchild_user):
                        tc = Tchild_user  
                        a = "In " + Tparent_user +" apart from "
                    else: 
                        tc = Tparent_user
                        a = "In "     

                    desc_temp['s'] = a + tc + ", perhaps you can explore these-\n" + res_sib
                    found_sib = 1
                
                if (found_sib and found_child): 

                    pick = random.sample(['c','s'],1)[0] # make a random choice

                elif found_sib:
                    pick = 's'

                else :
                    pick = 'c'
                
                
                # final desc

                desc += desc_temp[pick]

                # try to get children or siblings ----------end of block


            else: # for medium

                if (article): # already seen some articles
                    desc = h1.describe_research(TparentID, Tchild_grakn ,'1',topic_turn_r,topic_turn_w,content_type,intent)
                    topic_turn_r = topic_turn_r + 1

            # if desc is empty in know more: get some filler article

            if (len(desc) < 3): 
                desc += h1.describe_research(TparentID, Tchild_grakn ,'1',topic_turn_r,topic_turn_w,content_type,intent)
                topic_turn_r = topic_turn_r + 1

        else: # if not next level affirm (i.e. know_more)  


            # if (intent=='next_level_affirm' and topic_turn_w > 1): # switch content type to add variety

            if content_type=='wiki' and not Tchild_grakn:
                content_type = 'research'
            else: 
                content_type = 'wiki'

            positive = ["Awesome!", "Great,", "You got it!", "Wonderful,"]

            source_check = [" Checking other sources..", "Let me check more channels..", " Looking deeper.."]


            desc = random.sample(positive,1)[0] + random.sample(source_check,1)[0]




            if (content_type=='wiki'): 

                desc = ''

                if (topic_turn_w < 3): # first produce the list of subtopics
                    desc += h1.describe_wiki_Tparent(Tparent_grakn,'1',topic_turn_w,intent)
                
                    desc += "\n Would you like to know the latest research?" 
                    topic_turn_w = topic_turn_w + 1
                
                else: # get an additional child topic
                    desc += "\n Perhaps I can bring some extra details for you to read,\n"
                    additional_child_topic = random.sample(additional,1)[0] # pick a random add on topic
                    desc += h1.describe_wiki_Tchild(Tparent_grakn,additional_child_topic,'2',topic_turn_r,topic_turn_w,content_type,intent)

                    additional_child_topic = h1.get_Tchild_list(additional_child_topic,'','2')

                    additional_child_topic_desc = h1.process_result_bullets(additional_child_topic)
                    desc+= additional_child_topic_desc

                    if (len(desc) <3): 
                        desc = "Sorry, did not find much, May be we can start over? please say restart to do so."

    
            else: # look in medium

                desc_art = ''
                desc_art += h1.describe_research(TparentID, Tchild_grakn ,'1',topic_turn_r,topic_turn_w,content_type,intent).split(']')[0]
                desc += desc_art

                if (len(desc) > 3 and '-' in desc and '[' in desc):
                    article = desc.split('[')[0].split('-')[1].lstrip().rstrip()
                

                topic_turn_r = topic_turn_r + 1



        dispatcher.utter_message(text=desc)

        ## clear child for new instance

        return [SlotSet("article", article),SlotSet("topic_turn_r", topic_turn_r),SlotSet("topic_turn_w", topic_turn_w),SlotSet("content_type", content_type), SlotSet("TparentID", TparentID),SlotSet("current_level", new_level),SlotSet("Tchild_store", Tchild_grakn), SlotSet("Tchild", Tchild_user)]

class ActionS5(Action):

    def name(self) -> Text:
        return "action_research_open"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        desc = h1.dontknow()

        current_level = tracker.get_slot("current_level")

        current_level = str(current_level)

        if not current_level: 
            current_level = '1'
        else:
            new_level = int(current_level) + 1

        Tparent_user = tracker.get_slot("Tparent")

        Tparent_grakn = tracker.get_slot("Tparent_store")

        topic_turn_w = tracker.get_slot("topic_turn_w")

        topic_turn_r = tracker.get_slot("topic_turn_r")

        content_type = tracker.get_slot("content_type")

        TparentID = tracker.get_slot("TparentID")

        intent = tracker.latest_message['intent'].get('name')


        Tchild_grakn = ''

        if (not TparentID): 
            TparentID = h1.get_topicID(Tparent_grakn,'1')

        if (len(TparentID)): 

            desc = h1.describe_research(TparentID, Tchild_grakn,'1',topic_turn_r,topic_turn_w,content_type,intent)
            
            topic_turn_r = topic_turn_r + 1

            if (len(desc) > 3 and '-' in desc and '[' in desc):
                article = desc.split('[')[0].split('-')[1].lstrip().rstrip()
        

        dispatcher.utter_message(text=desc)

        ## clear child for new instance

        return [SlotSet("article", article),SlotSet("topic_turn_r", topic_turn_r),SlotSet("topic_turn_w", topic_turn_w),SlotSet("content_type", content_type), SlotSet("TparentID", TparentID),SlotSet("current_level", new_level),SlotSet("Tchild_store", None), SlotSet("Tchild", None)]
