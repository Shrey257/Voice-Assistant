import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import re
import tkinter as tk
import requests
import random
from tkinter import scrolledtext

# Initialize the assistant's voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set voice to female (optional)

# Schedule dictionary to store tasks and their timings
schedule = {}

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()
    update_gui(f"Assistant: {text}")

# Function to take voice commands from the user
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_gui("Listening...")
        recognizer.pause_threshold = 1  # Adjust the pause threshold based on ambient noise
        audio = recognizer.listen(source)

    try:
        update_gui("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')  # Use Google's speech recognition
        update_gui(f"User said: {command}\n")
    except Exception:
        update_gui("Say that again please...")
        return None
    return command.lower()

# Function to greet the user based on the time of the day
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")

# Function to add an activity to the schedule
def add_to_schedule(command):
    task = re.search(r'add (.*) at (.*)', command)
    if task:
        activity = task.group(1)
        time = task.group(2)
        schedule[time] = activity
        speak(f"Added {activity} at {time} to your schedule.")
    else:
        speak("I couldn't understand the time or activity. Please try again.")

# Function to remove an activity from the schedule
def remove_from_schedule(command):
    task = re.search(r'remove (.*) at (.*)', command)
    if task:
        activity = task.group(1)
        time = task.group(2)
        if time in schedule:
            del schedule[time]
            speak(f"Removed {activity} at {time} from your schedule.")
        else:
            speak(f"No activity found at {time}.")
    else:
        speak("I couldn't understand the time or activity. Please try again.")

# Function to show the schedule
def show_schedule():
    if schedule:
        update_gui("Here is your schedule:")
        for time, activity in schedule.items():
            update_gui(f"At {time}, you have {activity}.")
    else:
        update_gui("Your schedule is empty.")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why was the math book sad? Because it had too many problems."
    ]
    joke = random.choice(jokes)
    speak(joke)

def fun_fact():
    facts = [
        "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
        "Did you know? A day on Venus is longer than a year on Venus!",
        "Did you know? Octopuses have three hearts!"
    ]
    fact = random.choice(facts)
    speak(fact)

# Function to tell the current date
def tell_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {current_date}")

# Function to update GUI with text
def update_gui(text):
    output_box.insert(tk.END, text + "\n")
    output_box.yview(tk.END)

# Function to get weather information
def get_weather(city="Mumbai"):
    api_key = "your_api_key"  # Replace with OpenWeatherMap API Key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
    else:
        speak("Sorry, I couldn't retrieve the weather information.")

# Function to share a motivational quote
def daily_quote():
    quotes = [
        "Believe you can and you're halfway there.",
        "Don't watch the clock; do what it does. Keep going.",
        "The only way to do great work is to love what you do."
    ]
    quote = random.choice(quotes)
    speak(quote)

def calculate(expression):
    # Replace words with their mathematical operators
    expression = expression.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
    
    try:
        # Use eval to evaluate the mathematical expression
        result = eval(expression)
        speak(f"The result is {result}")
    except (SyntaxError, NameError):
        speak("Sorry, I couldn't understand the calculation.")
    except ZeroDivisionError:
        speak("Sorry, you can't divide by zero.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}. Sorry I couldnot calculate that")

# Main function to handle user commands
def execute_commands():
    command = take_command()
    if command is None:
        return

    # Perform different actions based on command
    if 'wikipedia' in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif 'motivate me' in command or 'quote' in command:
        daily_quote()
    elif 'open whatsapp web' in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web")
    elif 'the time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")
    elif 'the date' in command or 'what is the date' in command:
        tell_date()
    elif 'open notepad' in command:
        os.system("notepad.exe")
        speak("Opening Notepad")
    elif 'add' in command and 'at' in command:
        add_to_schedule(command)
    elif 'remove' in command and 'at' in command:
        remove_from_schedule(command)
    elif 'show schedule' in command:
        show_schedule()
    elif 'tell me a joke' in command:
        tell_joke()
    elif 'fun fact' in command:
        fun_fact()
    elif 'weather' in command:
        speak("Please specify the city.")
        city = take_command()
        get_weather(city)
    elif 'calculate' in command:
        speak("What would you like to calculate?")
        expression = take_command()
        calculate(expression)
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye! Have a nice day!")
        app.quit()

# GUI setup with Tkinter
app = tk.Tk()
app.title("Voice Assistant")
app.geometry("500x400")

# Scrolled text box for displaying conversation
output_box = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=15, font=("Arial", 10))
output_box.pack(pady=10)

# Buttons to control the assistant
btn_listen = tk.Button(app, text="Listen", command=execute_commands)
btn_listen.pack(pady=5)

btn_exit = tk.Button(app, text="Exit", command=app.quit)
btn_exit.pack(pady=5)

greet_user()  # Greet user at start

app.mainloop()
