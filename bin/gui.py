import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
from gpt4all import GPT4All
import pvporcupine
import pyaudio
import struct

# Load GPT4All model
model = GPT4All("Llama-3.2-1B-Instruct-Q4_K_M.gguf",
                model_path=r"C:\python programming\Personal assistant\models")

# Initialize TTS
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# GUI setup
root = tk.Tk()
root.title("Alex - Personal Assistant")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_box.pack(padx=10, pady=10)

# Porcupine wake word setup
access_key = "59/O/C2TXB7afvwBxwTyt5HZk7SZJZkhbdM5SrV+cwDmLenMnJ3Wfw=="  # replace with your key
keyword_path = r"C:\python programming\Personal assistant\bin\Alex.ppn"
porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[keyword_path])

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=porcupine.sample_rate,
                 input=True,
                 frames_per_buffer=porcupine.frame_length)

recognizer = sr.Recognizer()
mic = sr.Microphone()

def run_assistant(user_input):
    chat_box.insert(tk.END, f"You: {user_input}\n")
    try:
        with model.chat_session():
            response = model.generate(user_input, max_tokens=200)
        chat_box.insert(tk.END, f"Alex: {response}\n\n")
        chat_box.see(tk.END)
        speak(response)
    except Exception as e:
        chat_box.insert(tk.END, f"❌ Error: {e}\n\n")
        speak("Sorry, I had trouble generating a response.")

def wake_word_listener():
    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            chat_box.insert(tk.END, "👂 Wake word detected: Alex\n")
            listen_microphone()

def listen_microphone():
    try:
        with mic as source:
            chat_box.insert(tk.END, "🎤 Listening...\n")
            speak("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        user_input = recognizer.recognize_google(audio)
        run_assistant(user_input)
    except Exception as e:
        chat_box.insert(tk.END, f"❌ Voice Error: {e}\n\n")
        speak("Sorry, I couldn't understand that.")

# Start wake word listener in background thread
threading.Thread(target=wake_word_listener, daemon=True).start()

root.mainloop()