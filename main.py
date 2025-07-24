# nanoface_ai/main.py
import sys
import os
import json
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from threading import Thread
from audio.audio_manager import AudioManager
from api_clients.stt import STTClient
from api_clients.chat import ChatClient
from api_clients.tts import TTSClient
from api_clients.mood import MoodClient
from gui.settings_panel import SettingsPanel

CONFIG_PATH = "config.json"
FACE_PATH = "faces"

class FaceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NanoFace AI")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.settings_button = QPushButton("⚙", self)
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.move(10, 10)
        self.settings_button.clicked.connect(self.open_settings)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.config = self.load_config()
        self.api_clients = self.init_clients()
        self.audio_manager = AudioManager(self.config)

        self.settings_panel = SettingsPanel(self.config, self.api_clients, self.audio_manager)
        self.settings_panel.hide()

        self.current_mood = "muet"
        self.idle = True
        self.play_gif_loop()

        self.listen_thread = Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def load_config(self):
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as f:
                json.dump({}, f)
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

    def init_clients(self):
        return {
            "stt": STTClient(self.config),
            "chat": ChatClient(self.config),
            "tts": TTSClient(self.config),
            "mood": MoodClient(self.config)
        }

    def play_gif_loop(self):
        gifs = os.listdir(os.path.join(FACE_PATH, self.current_mood))
        gif = random.choice(gifs)
        movie = QMovie(os.path.join(FACE_PATH, self.current_mood, gif))
        self.label.setMovie(movie)
        movie.start()
        QTimer.singleShot(movie.duration(), self.play_gif_loop) if self.idle else None

    def open_settings(self):
        self.settings_panel.show()

    def listen_loop(self):
        while True:
            audio = self.audio_manager.listen()
            text = self.api_clients["stt"].transcribe(audio)
            if not text:
                continue
            mood = self.api_clients["mood"].get_mood(text)
            reply = self.api_clients["chat"].get_response(text)
            tts_audio = self.api_clients["tts"].synthesize(reply)

            self.current_mood = mood
            self.idle = False
            self.audio_manager.play(tts_audio)
            self.idle = True
            self.current_mood = "muet"
            self.play_gif_loop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceWindow()
    window.show()
    sys.exit(app.exec_())
