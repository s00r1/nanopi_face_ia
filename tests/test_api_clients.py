import requests
from api_clients.stt import STTClient
from api_clients.chat import ChatClient


class DummyResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}
        self.content = b''

    def json(self):
        return self._json


def test_stt_transcribe_without_config(tmp_path):
    client = STTClient({})
    assert client.transcribe(str(tmp_path / "dummy.wav")) == ""


def test_chatclient_success(monkeypatch):
    def fake_post(url, headers=None, json=None):
        return DummyResponse(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.setattr(requests, "post", fake_post)
    client = ChatClient({"chat_api_key": "k", "chat_api_url": "http://x"})
    assert client.get_response("hello") == "ok"
