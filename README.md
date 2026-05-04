# Alex – Personal Assistant Project

## 📌 Overview
Alex is a modular Python‑based personal assistant that has evolved through three versions:
1. **Alex 1.0** – Basic assistant without API integration  
2. **Alex 2.0** – Enhanced assistant with API support (Google Custom Search, GPT4All integration)  
3. **Alex GUI** – Dark neon‑themed graphical interface with wake‑word detection, voice input/output, and chat window  

---

## 📂 Project Structure
```
Personal assistant
├── bin
│   ├── alex1.0.py        # Basic assistant (no API)
│   ├── alex2.0.py        # API-enabled assistant
│   ├── gui.py            # GUI version (Tkinter + neon theme)
│   ├── Alex.ppn          # Wake-word file for Porcupine
│   └── ding.mp3          # Notification sound
└── models
    └── llama-3.2-1b-instruct-q4_0.gguf   # GPT4All model file
```

---

## ⚙️ Requirements
Install dependencies:
```bash
pip install gpt4all pyttsx3 SpeechRecognition pvporcupine pyaudio wikipedia requests flask
```

> **Notes:**  
> - `pyaudio` may require `pip install pipwin && pipwin install pyaudio` on Windows.  
> - You need a valid **Porcupine access key** from [Picovoice Console](https://console.picovoice.ai/).  
> - Place your GPT4All `.gguf` model inside the `models/` folder.  

---

## 🚀 Versions

### 🔹 Alex 1.0 – Basic Assistant
- Runs without external APIs.  
- Supports wake‑word detection, speech recognition, text‑to‑speech.  
- Commands: time/date, Wikipedia summaries, jokes, music playback, open apps.  
- Run:
```bash
python bin/alex1.0.py
```

---

### 🔹 Alex 2.0 – API‑Enabled Assistant
- Integrates **Google Custom Search API** for web queries.  
- Uses GPT4All for conversational replies.  
- Sends commands to a local Flask backend (optional).  
- Run:
```bash
python bin/alex2.0.py
```

---

### 🔹 Alex GUI – Dark Neon Interface
- Tkinter GUI with neon styling (green, pink, blue).  
- Wake‑word detection via Porcupine (`Alex.ppn`).  
- Voice input/output with SpeechRecognition + pyttsx3.  
- Chat window shows conversation history.  
- Run:
```bash
python bin/gui.py
```

---

## 🔑 Configuration
- **Wake word file**: Place `Alex.ppn` inside `bin/` and update the path in code.  
- **Model file**: Download a GPT4All `.gguf` model (e.g., *Llama 3.2 1B Instruct*) and place it inside `models/`.  
- **Access key**: Replace `access_key` in scripts with your Porcupine key.  
- **API key (Alex 2.0)**: Add your Google Custom Search API key in `alex2.0.py`.  

---

## 🛠️ Features Across Versions
- Wake‑word detection (“Alex”)  
- Voice input/output  
- Conversational replies via GPT4All  
- API‑based web search (Alex 2.0)  
- GUI with neon theme (Alex GUI)  
- Basic commands: time/date, Wikipedia, jokes, music, open apps, shutdown  

---

## 📌 Notes
- **Alex 1.0** is lightweight and offline.  
- **Alex 2.0** adds API integration for richer responses.  
- **Alex GUI** provides a futuristic neon interface with wake‑word and voice interaction.  

---
