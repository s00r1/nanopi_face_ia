# gui/settings_panel.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QSlider, QGroupBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import json

CONFIG_PATH = "config.json"

class SettingsPanel(QWidget):
    def __init__(self, config, api_clients, audio_manager):
        super().__init__()
        self.config = config
        self.api_clients = api_clients
        self.audio_manager = audio_manager
        self.setWindowTitle("Paramètres")
        self.setGeometry(100, 100, 400, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.build_api_settings()
        self.build_audio_settings()
        self.build_buttons()

    def build_api_settings(self):
        self.api_inputs = {}
        for key in ["stt", "tts", "chat", "mood"]:
            group = QGroupBox(f"API {key.upper()}")
            layout = QVBoxLayout()

            key_input = QLineEdit()
            key_input.setPlaceholderText("API Key")
            key_input.setText(self.config.get(f"{key}_api_key", ""))
            layout.addWidget(key_input)

            model_input = QLineEdit()
            model_input.setPlaceholderText("Model ID")
            model_input.setText(self.config.get(f"{key}_model", ""))
            layout.addWidget(model_input)

            self.api_inputs[f"{key}_api_key"] = key_input
            self.api_inputs[f"{key}_model"] = model_input

            group.setLayout(layout)
            self.layout.addWidget(group)

    def build_audio_settings(self):
        group = QGroupBox("Audio")
        layout = QVBoxLayout()

        # Input
        self.input_selector = QComboBox()
        inputs = self.audio_manager.list_input_devices()
        for idx, name in inputs:
            self.input_selector.addItem(name, idx)
        self.input_selector.currentIndexChanged.connect(self.change_input)
        layout.addWidget(QLabel("Microphone:"))
        layout.addWidget(self.input_selector)

        self.mic_slider = QSlider(Qt.Horizontal)
        self.mic_slider.setRange(0, 100)
        self.mic_slider.setValue(70)
        self.mic_slider.sliderReleased.connect(self.set_mic_volume)
        layout.addWidget(QLabel("Volume Micro:"))
        layout.addWidget(self.mic_slider)

        # Output
        self.output_selector = QComboBox()
        outputs = self.audio_manager.list_output_devices()
        for idx, name in outputs:
            self.output_selector.addItem(name, idx)
        self.output_selector.currentIndexChanged.connect(self.change_output)
        layout.addWidget(QLabel("Haut-parleur:"))
        layout.addWidget(self.output_selector)

        self.out_slider = QSlider(Qt.Horizontal)
        self.out_slider.setRange(0, 100)
        self.out_slider.setValue(70)
        self.out_slider.sliderReleased.connect(self.set_out_volume)
        layout.addWidget(QLabel("Volume Haut-parleur:"))
        layout.addWidget(self.out_slider)

        group.setLayout(layout)
        self.layout.addWidget(group)

    def build_buttons(self):
        self.save_btn = QPushButton("Sauvegarder")
        self.save_btn.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_btn)

        self.scan_btn = QPushButton("Rescanner périphériques")
        self.scan_btn.clicked.connect(self.refresh_devices)
        self.layout.addWidget(self.scan_btn)

    def change_input(self):
        device_index = self.input_selector.currentData()
        self.audio_manager.set_input_device(device_index)

    def change_output(self):
        device_index = self.output_selector.currentData()
        self.audio_manager.set_output_device(device_index)

    def set_mic_volume(self):
        volume = self.mic_slider.value()
        self.audio_manager.set_volume(volume, output=False)

    def set_out_volume(self):
        volume = self.out_slider.value()
        self.audio_manager.set_volume(volume, output=True)

    def refresh_devices(self):
        self.input_selector.clear()
        for idx, name in self.audio_manager.list_input_devices():
            self.input_selector.addItem(name, idx)
        self.output_selector.clear()
        for idx, name in self.audio_manager.list_output_devices():
            self.output_selector.addItem(name, idx)

    def save_config(self):
        for key, widget in self.api_inputs.items():
            self.config[key] = widget.text()
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)
        self.hide()
