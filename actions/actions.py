# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSuggestExercise(Action):
    def name(self) -> Text:
        return "action_suggest_exercise"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weakness = tracker.get_slot("weakness")

        user_level = ''.join(filter(str.isdigit, tracker.get_slot("level")))[:1]

        level_range = [int(user_level) - 1, int(user_level), int(user_level) + 1]

        exercise = self.exercises_collection.find_one({
            "level": {"$in": level_range},
            "tags": weakness
        })
        if exercise:
            message = f"Hier ist eine Übung für dich: {exercise['name']} - {exercise['description']}"
        else:
            message = "Leider habe ich keine Übung für dein Level gefunden." + user_level + weakness

        dispatcher.utter_message(text=message)
        return []


class ActionSuggestExerciseByType(Action):
    def name(self) -> Text:
        return "action_suggest_exercise_by_type"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        askexercise = tracker.get_slot("askExercise")

        exercise = self.exercises_collection.find_one({"tags": askexercise})

        if exercise:
            message = f"Hier ist eine Übung für {askexercise}: {exercise['name']} - {exercise['description']}"
        else:
            message = f"Leider habe ich keine Übung für {askexercise} gefunden."

        dispatcher.utter_message(text=message)
        return []
