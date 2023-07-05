import openai
import configparser
from gtts import gTTS
from playsound import playsound

config = configparser.ConfigParser()
config.read("config.ini")

openai.api_key = str(config["USER"]["OPENAI_KEY"])

messages = [
    {"role": "system", "content": "You are a an AI Assistant"},
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


query = ""
while True:
    query = input("Ask something: ")
    if query == "e":
        break
    reply = chatgpt(query)
    print(f"> {reply}")
    speech = gTTS(text = reply)
    speech.save('reply.mp3')
    playsound('reply.mp3')