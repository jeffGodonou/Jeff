# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Get location from the tracker
        location = tracker.get_slot("location")
        date = tracker.get_slot("date")
        message = f"The weather in {location} at {date}."

        # OpenWeatherMap API key
        api_key = '7f88e0b55a9fa291a1b2854af083a0e3'
        # Units specify the desired units (e.g., 'metric' for Celsius and 'imperial' for Farheinheit)
        units = 'metric'

        # Make a request to the OpenWeatherMap API
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid={api_key}'
        response = requests.get(weather_url)
        weather_data = response.json()

        # Extract relevant information from the API response
        temperature = weather_data.get('main', {}).get('temp')
        description = weather_data.get('weather', [{}])[0].get('description')

        # Respond to the user
        if temperature and description:
            message = f"The weather in {location} is {description} with a temperature of {temperature} degrees Celsius."
        else:
            message = "I'm sorry, I couldn't retrieve the weather information at the moment."

        dispatcher.utter_message(message)

        return []
