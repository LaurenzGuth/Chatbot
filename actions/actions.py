import json
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .exercise_history import ExerciseHistory


class ActionSuggestExercise(Action):
    def name(self) -> Text:
        return "action_suggest_exercise"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]
        self.history = ExerciseHistory()
        self.load_data_from_json("db/exercises.json")

    def load_data_from_json(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.exercises_collection.delete_many({})
            self.exercises_collection.insert_many(data)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weakness = tracker.get_slot("weakness")
        user_level = ''.join(filter(str.isdigit, tracker.get_slot("level")))[:1]
        level_range = [int(user_level) - 1, int(user_level), int(user_level) + 1]

        exercise = self.exercises_collection.find_one({
            "level": {"$in": level_range},
            "tags": weakness,
            "_id": {"$nin": self.history.get_last_exercises()}
        })

        if exercise:
            self.history.add_exercise(exercise["_id"])
            message = f"Hier ist eine Übung für dich: {exercise['name']} - {exercise['description']}"
        else:
            message = "Leider habe ich keine Übung für dein Level gefunden."

        dispatcher.utter_message(text=message)
        return []


class ActionSuggestExerciseByType(Action):
    def name(self) -> Text:
        return "action_suggest_exercise_by_type"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]
        self.history = ExerciseHistory()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weakness = tracker.get_slot("weakness")

        exercise = self.exercises_collection.find_one({
            "tags": weakness,
            "_id": {"$nin": self.history.get_last_exercises()}
        })

        if exercise:
            self.history.add_exercise(exercise["_id"])
            message = f"Hier ist eine Übung für {weakness}: {exercise['name']} - {exercise['description']}"
        else:
            message = f"Leider habe ich keine Übung für {weakness} gefunden."

        dispatcher.utter_message(text=message)
        return []


class ActionSuggestAnotherExercise(Action):
    def name(self) -> Text:
        return "action_suggest_another_exercise"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]
        self.history = ExerciseHistory()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weakness = tracker.get_slot("weakness")

        try:
            user_level = int(tracker.get_slot("level")[0])
        except (TypeError, ValueError, IndexError):
            user_level = 42
        exercise = self.exercises_collection.find_one({
            "tags": weakness,
            "_id": {"$nin": self.history.get_last_exercises()}
        })

        if exercise:
            self.history.add_exercise(exercise["_id"])
            if exercise['level'] > user_level & user_level != 42:
                message = (
                    f"Hier ist eine weitere Übung für {weakness}: {exercise['name']} - {exercise['description']} "
                    f"Bedenke, dass diese Übung ein höheres Level hat! Übungslevel: {exercise['level']}")
            else:
                message = f"Hier ist eine weitere Übung für {weakness}: {exercise['name']} - {exercise['description']}"
        else:
            message = f"Leider habe ich keine weitere Übung für {weakness} gefunden."

        dispatcher.utter_message(text=message)
        return []


class ActionGetDetails(Action):
    def name(self) -> Text:
        return "action_get_detail"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["exercise_database"]
        self.exercises_collection = self.db["exercises"]
        self.history = ExerciseHistory()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        details = tracker.get_slot("detail").lower()
        last_exercise_id = self.history.get_last_exercises()[-1]

        exercise = self.exercises_collection.find_one({"_id": last_exercise_id})

        if details == "level":
            message = f"Die Schwierigkeit der Übung {exercise['name']} ist {exercise['level']}."
        elif details == "beschreibung":
            message = f"Die Beschreibung der Übung {exercise['name']} lautet: {exercise['description']}."
        elif details == "tags":
            message = f"Die Tags der Übung {exercise['name']} sind: {', '.join(exercise['tags'])}."
        elif details == "video":
            if "video" in exercise and exercise["video"]:
                message = f"Hier ist ein Video zur Übung {exercise['name']}: {exercise['video']}"
            else:
                message = f"Leider gibt es kein Video zur Übung {exercise['name']}."
        elif details == "tipps":
            if "tips" in exercise and exercise["tips"]:
                message = f"Hier ist ein Tipp zur Übung {exercise['name']}: {exercise['tips']}"
            else:
                message = f"Leider gibt es keine Tipps zur Übung {exercise['name']}."
        else:
            message = f"Ich konnte keine {details} zu dieser Übung finden."

        dispatcher.utter_message(text=message)
        return []


class ActionTellAJoke(Action):
    def name(self) -> Text:
        return "action_tell_a_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import requests

        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            joke_text = f"{joke['setup']} {joke['punchline']}"
        else:
            joke_text = "Ich konnte keinen Witz finden, versuche es später noch einmal."

        dispatcher.utter_message(text=joke_text)

        return []


class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        import requests

        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d02948c3d14f29d8f64f6dd3a92fd499")
        if response.status_code == 200:
            weather = response.json()
            weather_text = f"Das Wetter in {city} ist {weather['weather'][0]['description']}."
        else:
            weather_text = "Ich konnte keine Wetterinformationen finden, versuche es später noch einmal."

        dispatcher.utter_message(text=weather_text)

        return []
