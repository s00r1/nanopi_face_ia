# api_clients/chat.py

import requests

class ChatClient:
    def __init__(self, config):
        self.api_key = config.get("chat_api_key")
        self.endpoint = config.get("chat_api_url")
        self.model = config.get("chat_model", "default")

    def get_response(self, prompt):
        headers = {'Authorization': f"Bearer {self.api_key}", 'Content-Type': 'application/json'}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return ""
