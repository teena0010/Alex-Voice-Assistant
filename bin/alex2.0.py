import pvporcupine
import pyaudio
import struct
import pyttsx3
import speech_recognition as sr
import requests
import time
from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct-Q4_K_M.gguf",
                model_path=r"C:\python programming\Personal assistant\models")

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
        try:
            command = listener.recognize_google(audio).lower()
            print("✅ Command received:", command)
            run_assistant(command)
        except Exception as e:
            print("❌ Error:", e)
            speak("Sorry, I didn't understand that.")

def run_assistant(command):
    try:
        # Start a chat session with GPT4All
        with model.chat_session():
            response = model.generate(command, max_tokens=200)

        print("🧠 Response:", response)
        speak(response)

    except Exception as e:
        print("❌ GPT4All Error:", e)
        speak("Sorry, I had trouble generating a response.")


# Replace with your actual access key from Picovoice Console
access_key = "59/O/C2TXB7afvwBxwTyt5HZk7SZJZkhbdM5SrV+cwDmLenMnJ3Wfw=="
import os

keyword_path = r"C:\python programming\Personal assistant\bin\Alex.ppn"

porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths=[keyword_path]
)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=porcupine.sample_rate,
                 input=True,
                 frames_per_buffer=porcupine.frame_length)

print("🔊 Assistant is running. Say 'Alex' to activate.")

try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("👂 Wake word detected!")
            speak("Yes?")
            listen_for_command()
except KeyboardInterrupt:
    print("🛑 Stopping assistant...")
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()