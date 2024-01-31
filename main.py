import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import time
import random
import numpy as np
from cybernews.cybernews import CyberNews
import requests

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Vishal: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        time.sleep(0.2)
        r.pause_threshold = 1.5
        audio = r.listen(source,timeout=2,phrase_time_limit=10)

        try:
            print("Recognizing...\n")
            time.sleep(0.5)
            query = r.recognize_google(audio , language='en-in')
            print(f"User said : {query}")
    
        except Exception as e:
            say("Sorry! Can't able to understand you! Say that again please!...")
            return "none"
    
        return query
       
if __name__ == '__main__':
    say("Hello I am Jarvis A.I.")
    say("Here is some top news of the day of cyberspace")

    news = CyberNews()

    top_news = news.get_news("general")[0]['headlines']
    say(top_news)

    while True:
        print('listening')
        query = takeCommand().lower()
        print(query)
        sites = [["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.com"],["google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                webbrowser.open(site[1])

        if "open FaceTime" in query:
            facetimePath="/System/Applications/FaceTime.app"
            os.system(f"open {facetimePath}")

        if "open spotify" in query:
            spotifyPath="/Applications/Spotify.app"
            os.system(f"open {spotifyPath}")

        if "open photos" in query:
            photosPath="/System/Applications/Photos.app"
            os.system(f"open {photosPath}")

        if "open discord" in query:
            discordPath="/Applications/Discord.app"
            os.system(f"open {discordPath}")

        if "open notes" in query:
            notesPath="/System/Applications/Notes.app"
            os.system(f"open {notesPath}")

        if "ip address" in query.lower():
            ip = requests.get('https://api.ipify.org').text
            say(f"Your IP Address is : {ip}")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)