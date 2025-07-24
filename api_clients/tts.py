# api_clients/tts.py

import requests
import uuid

class TTSClient:
    def __init__(self, config):
        self.api_key = config.get("tts_api_key")
        self.endpoint = config.get("tts_api_url")
        self.model = config.get("tts_model", "default")

    def synthesize(self, text):
        headers = {'Authorization': f"Bearer {self.api_key}", 'Content-Type': 'application/json'}
        data = {
            "model": self.model,
            "input": text
        }
        response = requests.post(self.endpoint, json=data, headers=headers)
        if response.status_code == 200:
            out_path = f"/tmp/tts_{uuid.uuid4().hex}.wav"
            with open(out_path, "wb") as f:
                f.write(response.content)
            return out_path
        return None
