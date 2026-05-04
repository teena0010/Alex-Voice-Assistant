import pvporcupine         #wake word detection
import pyaudio             #microphone input
import struct              #converts raw audio to usable format
import pyttsx3             #text to speech
import pywhatkit           #plays youtube videos
import datetime            #gets current time
import wikipedia           #fetches summaries
import pyjokes             #tells jokes
import speech_recognition as sr       #converts speech to text
import time
import os

# Initialize speech engine
#engine = pyttsx3.init()
#engine.setProperty('voice', engine.getProperty('voices')[0].id)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[0].id)        # sets the voice
    engine.say(text)      # speaks aloud
    engine.runAndWait()


def listen_for_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:        #sets the microphone as listening input source
        print("🎤 Listening for command...")
        listener.adjust_for_ambient_noise(source)          #ignores background noises
        audio = listener.listen(source)
        try:
            command = listener.recognize_google(audio).lower()      #recognizes the command
            print("✅ Command received:", command)
            run_assistant(command)
        except Exception as e:
            print("❌ Error:", e)
            speak("Sorry, I didn't understand that.")

def run_assistant(command):
    if 'play' in command:
        song = command.replace('play', '')
        speak('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time)
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%A, %d %B %Y')
        speak('Today is ' + date)
    elif 'who is' in command:
        name = command.replace('who is', '')
        info = wikipedia.summary(name, 2)
        print(info)
        speak(info)
    elif 'what is' in command:
        matter = command.replace('what is', '')
        info = wikipedia.summary(matter, 2)
        print(info)
        speak(info)
    elif 'tell me about' in command:
        tell = command.replace('tell me about', '')
        info = wikipedia.summary(tell, 2)
        print(info)
        speak(info)
    elif 'joke' in command:
        speak(pyjokes.get_joke())
    elif 'search for' in command:
        query = command.replace('search for', '')
        speak('Searching for ' + query)
        pywhatkit.search(query)
    elif 'open youtube' in command:
        speak('Opening YouTube')
        pywhatkit.playonyt("YouTube")
    elif 'open google' in command:
        speak('Opening Google')
        pywhatkit.search("Google")
    elif 'open calculator' in command:
        speak('Opening Calculator')
        os.system("calc.exe")
    elif 'open notepad' in command:
        speak('Opening Notepad')
        os.system("notepad.exe")
    elif 'shutdown' in command or 'exit' in command or 'stop' in command:
        speak("Shutting down. Goodbye!")
        exit()
    else:
        speak("I didn't catch that. Can you repeat?")

# Replace with your actual access key from Picovoice Console
access_key = "your_api_key"

porcupine = pvporcupine.create(access_key=access_key, keyword_paths=["Alex.ppn"])
pa = pyaudio.PyAudio()        #- Initializes PyAudio, which lets you access your microphone for audio input.
stream = pa.open(format=pyaudio.paInt16,         #- Opens an audio stream for real-time listening.
                 channels=1,                     #16-bit audio format, Mono audio.
                 rate=porcupine.sample_rate,     #Uses the sample rate required by Porcupine.
                 input=True,                     #Enables microphone input.
                 frames_per_buffer=porcupine.frame_length)         #Number of audio samples per frame.

print("🔊 Assistant is running. Say 'Alex' to activate.")
#speak("Testing voice output")

try:
    while True:
        pcm = stream.read(porcupine.frame_length)                      #Reads a chunk of audio data from the microphone
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)    #- Converts the raw byte data into a tuple of 16-bit integers ("h" = short).
        keyword_index = porcupine.process(pcm)                         #Feeds the audio frame into Porcupine to check for the wake word.
        if keyword_index >= 0:                                         #- Returns -1 if no keyword is detected, or an index (e.g., 0) if detected.
            print("👂 Wake word detected!")
            speak("Yes?")
            listen_for_command()  # This runs once, then returns to wake word listening

except KeyboardInterrupt:
    print("🛑 Stopping assistant...")
finally:
    stream.stop_stream()              #Stops and closes the audio stream.
    stream.close()
    pa.terminate()                    #Terminates PyAudio.
    porcupine.delete()                #Deletes the Porcupine instance.
