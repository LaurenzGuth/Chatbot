# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSuggestExercise(Action):
    def name(self) -> Text:
        return "action_suggest_exercise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot("level")
        weakness = tracker.get_slot("weakness")

        # Hier Logik zur Auswahl der Übung
        exercise = f"Eine passende Übung für {level} Boulderer mit Fokus auf {weakness}"

        dispatcher.utter_message(text=f"Für dein {level} Level und deine Schwäche {weakness}, empfehle ich: {exercise}")
        return []