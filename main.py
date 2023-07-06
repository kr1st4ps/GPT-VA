import openai
import configparser
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

config = configparser.ConfigParser()
config.read("config.ini")

recognizer = sr.Recognizer()

openai.api_key = str(config["USER"]["OPENAI_KEY"])

messages = [
    {"role": "system", "content": config["AI"]["INSTRUCTIONS"]},
]

def chatgpt(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


query = None
reply = None
while True:
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        reply = "Sorry, I could not understand audio."

    print(f"<User> {query}")

    if not reply:
        reply = chatgpt(query)
    
    speech = gTTS(text = reply)
    speech.save('reply.mp3')
    print(f"<AI> {reply}")
    playsound('reply.mp3')
    
    query = None
    reply = None
    