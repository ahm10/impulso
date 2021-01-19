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


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        current_level=str(1)    
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

        return [SlotSet("Tparent_store", None), SlotSet("Tparent", None),SlotSet("Tchild_store", None), SlotSet("Tchild", None),SlotSet("current_level", None)]


class ActionReset(Action):

    def name(self) -> Text:
        return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            

        dispatcher.utter_message(text="Reset successful. Say Hi to initiate a conversation!")

        return [SlotSet("Tparent_store", None), SlotSet("Tparent", None),SlotSet("Tchild_store", None), SlotSet("Tchild", None),SlotSet("current_level", None)]



class ActionS(Action):

    def name(self) -> Text:
        return "action_s"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            

        dispatcher.utter_message(text="jsn!")

        return [SlotSet("Tparent_store", None), SlotSet("Tparent", None),SlotSet("Tchild_store", None), SlotSet("Tchild", None)]


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

        current_level = str(1)    
            
        Tparent_val = tracker.get_slot("Tparent")

        Tchild_val = tracker.get_slot("Tchild")

        # process the user input value

        Tparent_vals = h1.validate_Tparent_name(Tparent_val,current_level)

        Tparent_grakn = Tparent_vals['grakn']

        Tparent_user = Tparent_vals['user']

        desc = h1.describe0(Tparent_grakn,current_level)

        desc = desc + "\n\n Would you like to continue discussing " + Tparent_user + " (yes/no)?"

        dispatcher.utter_message(text=desc)

        return [SlotSet("current_level", current_level),SlotSet("Tparent_store", Tparent_grakn), SlotSet("Tparent", Tparent_user)]


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

        current_level = str(1)

        asked_level = str(2)
            
        Tparent_grakn = tracker.get_slot("Tparent_store")

        Tparent_user = tracker.get_slot("Tparent")

        Tchild_val = tracker.get_slot("Tchild")

        Tchild_vals = h1.validate_Tchild_name(Tparent_grakn,Tchild_val,asked_level)

        Tchild_grakn = Tchild_vals['grakn']

        Tchild_user = Tchild_vals['user']

        desc = ''

        desc += Tchild_vals['grakn']

        # if (Tchild_grakn): # found valid match

        #     desc += h1.describe1(Tparent_grakn,Tchild_grakn,current_level)

        # else: 
        #     desc += "\n I have trouble finding this.."
        
                # check for continuation

        desc += "\n would you like to continue on " + Tparent_user + "?"


        dispatcher.utter_message(text=desc)

        ## clear child for new instance

        return [SlotSet("current_level", current_level),SlotSet("Tchild_store", None), SlotSet("Tchild", None)]


 



        # return []

        # return [SlotSet("Tchild", Tchild_user)]


###### when you want to clear the Tparent
        #return [SlotSet("Tparent", None)] 
