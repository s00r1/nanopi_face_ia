# audio/audio_manager.py

import sounddevice as sd
import numpy as np
import wave
import os
import alsaaudio
import uuid

class AudioManager:
    def __init__(self, config):
        self.config = config
        self.input_device = None
        self.output_device = None
        self.sample_rate = 16000
        self.channels = 1
        self.duration = 5  # default duration if not listening continuously
        self.update_devices()

    def update_devices(self):
        devices = sd.query_devices()
        self.input_devices = [d for d in devices if d['max_input_channels'] > 0]
        self.output_devices = [d for d in devices if d['max_output_channels'] > 0]

    def list_input_devices(self):
        return [(i, d['name']) for i, d in enumerate(sd.query_devices()) if d['max_input_channels'] > 0]

    def list_output_devices(self):
        return [(i, d['name']) for i, d in enumerate(sd.query_devices()) if d['max_output_channels'] > 0]

    def set_input_device(self, index):
        self.input_device = index

    def set_output_device(self, index):
        self.output_device = index

    def set_volume(self, volume_percent, output=True):
        try:
            mixer = alsaaudio.Mixer(control='PCM' if output else 'Mic')
            mixer.setvolume(int(volume_percent))
        except alsaaudio.ALSAAudioError:
            print("Erreur: Impossible de régler le volume (alsa)")

    def record_audio(self, output_path, duration=None):
        duration = duration or self.duration
        print(f"[AudioManager] Recording {duration}s from input #{self.input_device}")
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            device=self.input_device
        )
        sd.wait()
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(recording.tobytes())
        return output_path

    def play_audio(self, file_path):
        print(f"[AudioManager] Playing audio {file_path} on output #{self.output_device}")
        try:
            with wave.open(file_path, 'rb') as wf:
                def callback(outdata, frames, time, status):
                    data = wf.readframes(frames)
                    if len(data) == 0:
                        raise sd.CallbackStop()
                    outdata[:] = np.frombuffer(data, dtype='int16').reshape(-1, self.channels)

                with sd.OutputStream(
                    samplerate=wf.getframerate(),
                    channels=wf.getnchannels(),
                    dtype='int16',
                    callback=callback,
                    device=self.output_device
                ):
                    sd.sleep(int(wf.getnframes() / wf.getframerate() * 1000))
        except Exception as e:
            print("Erreur lecture audio:", e)

    def listen(self, duration=None):
        """Enregistre un fichier audio temporaire et renvoie son chemin."""
        tmp_path = f"/tmp/listen_{uuid.uuid4().hex}.wav"
        return self.record_audio(tmp_path, duration)

    def play(self, file_path):
        """Lecture d'un fichier audio puis suppression du fichier."""
        self.play_audio(file_path)
        try:
            os.remove(file_path)
        except OSError:
            print(f"Erreur: impossible de supprimer {file_path}")

    def scan_audio_devices(self):
        return {
            "inputs": self.list_input_devices(),
            "outputs": self.list_output_devices()
        }
