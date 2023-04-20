import subprocess,time
import os
import pyttsx3 
import speech_recognition as sr
import datetime
import pyautogui
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Veronica Sir. Please tell me how may I help you")       

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        speak("Say that again please...")  
        return "None"
    return query

def get_temperature():
    api_key = "6b772de4746db4e610a7d070cc6f15d7" 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Jalandhar"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_celsius = current_temperature - 273.15
        return current_temperature_celsius
    else:
        return None

if __name__ == "__main__":
    wishMe()
    bulb_on = False
    bulb_turned_on_time = None
    while True:
        query = takeCommand().lower()
        if 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        
        elif 'turn on the bulb' in query:
            if not bulb_on:
                speak(f"The bulb is turned ONN")
                bulb_on = True
                bulb_turned_on_time = time.time()
            else:
                speak(f"The bulb is already ONN")
                
        elif 'turn off the bulb' in query:
            if bulb_on:
                speak(f"The bulb is turned OFF")
                bulb_on = False
                bulb_turned_on_time = None
            else:
                speak(f"The bulb is already OFF")
        
        elif 'what is the current temperature' in query:
            current_temperature = get_temperature()
            if current_temperature:
                speak(f"The current temperature is {round(current_temperature, 2)} degree Celsius")
            else:
                speak("Sorry, I couldn't retrieve the temperature at this time.")
        
        if bulb_turned_on_time and time.time() - bulb_turned_on_time >= 1800:
            
             print("bulb has been turned off")
        else:
            print("bulb has already been off")
