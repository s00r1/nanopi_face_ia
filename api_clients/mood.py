# api_clients/mood.py

import requests

class MoodClient:
    def __init__(self, config):
        self.api_key = config.get("mood_api_key")
        self.endpoint = config.get("mood_api_url")
        self.model = config.get("mood_model", "default")

    def get_mood(self, text):
        headers = {'Authorization': f"Bearer {self.api_key}", 'Content-Type': 'application/json'}
        data = {
            "model": self.model,
            "input": text
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("mood", "muet")
        return "muet"
