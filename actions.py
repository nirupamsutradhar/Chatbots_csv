# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.forms import FormAction
import requests

import re
import pandas as pd

subject = None
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = [{"title": "Certificate - 6 months", "payload": "/CourseDetails{\"subject\": \"Certificate - 6 months\"}"},
                   {"title": "O-Level (Diploma) - 12 months",
                    "payload": "/CourseDetails{\"subject\": \"O-Level (Diploma) - 12 months\"}"},
                   {"title": "A-level (Advanced) - 18 months",
                    "payload": "/CourseDetails{\"subject\": \"A-level (Advanced) - 18 months\"}"},
                   {"title": "Python/Data Science/Java/C++ - 12 months", "payload": "/CourseDetails{\"subject\": \"Python/Data Science/Java/C++ - 12 months\"}"}]

        dispatcher.utter_message(
            text="Hi! Welcome to  Data-Q - NIELIT Computer Center 🙂 ")
        dispatcher.utter_message(
            text="Glad you are excited to take your career to the next level. How ")
        dispatcher.utter_message(
            text="Which computer course you are interested for  ? ", buttons=buttons)

        return [UserUtteranceReverted()]


class ActionCommunicationMode(Action):

    def name(self) -> Text:
        return "action_communication_mode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global subject
        subject = tracker.get_slot("subject")
        print(subject)
        buttons = [{"title": "Email", "payload": "/CommunicationMode{\"Communication\":\"Email\"}"},
                   {"title": "Phone", "payload": "/CommunicationMode{\"Communication\":\"Phone\"}"}]

        dispatcher.utter_message(
            text="Please let us know your preferred means of communication to share the details of the courses.", buttons=buttons)

        return [UserUtteranceReverted()]


class ActionDetails(FormAction):

    def name(self) -> Text:
        return "detailform"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["comndetails", "name"]

    def validate_comndetails(self, value: Text,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: Dict[Text, Any],) -> Dict[Text, Any]:
        Communication = tracker.get_slot("Communication")
        print(value)
        if (Communication == "Email"):
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if(re.search(regex,value)):
                return {"comndetails": value}
            else:
                print("Emale prolknlk")
                dispatcher.utter_message(template="utter_wrong_email")
                return {"comndetails": None}

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []


class ActionSaveDetails(Action):

    def name(self) -> Text:
        return "action_save_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        Communication = tracker.get_slot("Communication")
        comnmode = tracker.get_slot("comndetails")

        print(name, Communication, comnmode, subject)

        dict = {'name': [name], 'Communication Medium': [
            Communication], 'Contact details': [comnmode], 'Subject': [subject]}

        df = pd.DataFrame(dict)
        df.to_csv('datafile.csv', mode='a', header=False)
        return []
