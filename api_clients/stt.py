# api_clients/stt.py

import requests

class STTClient:
    def __init__(self, config):
        self.api_key = config.get("stt_api_key")
        self.endpoint = config.get("stt_api_url")

    def transcribe(self, wav_path):
        if not self.api_key or not self.endpoint:
            return ""
        files = {'file': open(wav_path, 'rb')}
        headers = {'Authorization': f"Bearer {self.api_key}"}
        response = requests.post(self.endpoint, files=files, headers=headers)
        if response.status_code == 200:
            return response.json().get("text", "")
        return ""
