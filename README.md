# NanoFace AI 🎭🧠

Une interface vocale interactive pour NanoPi Neo + écran tactile SPI.
Posez-lui une question à la voix — il vous répond avec le bon ton… et le bon visage animé !

---

## 🔧 Matériel requis

- NanoPi Neo / RPi compatible
- Écran SPI 2.8" (affichage tactile compatible X11)
- Micro USB
- Haut-parleur USB ou DAC compatible ALSA
- `.gif` animés pour les visages (cf. structure ci-dessous)

---

## ⚙️ Installation des dépendances

### Paquets système

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-pyqt5 python3-numpy \
     python3-sounddevice python3-alsaaudio python3-requests
```

### Bibliothèques Python

```bash
pip3 install PyQt5 sounddevice numpy pyalsaaudio requests
```

---

## 🚀 Lancement de l'application

Assurez-vous de disposer d'un répertoire `faces/` contenant au moins un dossier par humeur (ex. `muet`, `joie`, `colere`, etc.) avec des fichiers `.gif`.
Copiez d'abord `config.example.json` vers `config.json` puis remplissez les clefs et URLs correspondant à vos services. Sans ce fichier, un `config.json` vide sera créé au premier démarrage.
```bash
python3 main.py
```

---

## 📁 Structure des dossiers

- `faces/` : animations classées par humeur.
- `api_clients/` : clients pour les API STT, TTS, Chat et Mood.
- `audio/` : enregistrement et lecture audio.
- `gui/` : panneau de réglages PyQt5.
- `main.py` : lance l'interface.
- `requirements.txt` : dépendances optionnelles.

Exemple minimal pour `faces/` :

```
faces/
├── muet/
│   └── idle.gif
├── joie/
│   └── smile.gif
```

---

## 📝 Exemple de configuration (`config.json`)

```json
{
  "stt_api_key": "VOTRE_CLE",
  "stt_api_url": "https://exemple.com/stt",
  "tts_api_key": "VOTRE_CLE",
  "tts_api_url": "https://exemple.com/tts",
  "chat_api_key": "VOTRE_CLE",
  "chat_api_url": "https://exemple.com/chat",
  "mood_api_key": "VOTRE_CLE",
  "mood_api_url": "https://exemple.com/mood",
  "tts_model": "v1",
  "chat_model": "v1",
  "mood_model": "v1"
}
```

Vous pouvez modifier ces valeurs via le panneau de paramètres accessible depuis
l'interface principale.
