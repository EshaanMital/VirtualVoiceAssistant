import tkinter as tk
import speech_recognition as sr
from gtts import *
import os
import datetime
import playsound
import pyjokes
import webbrowser
import tqdm
import wikipedia
import requests
import json

def get_audio():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            said = r.recognize_google(audio)
            print(said)
            return said
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        speak("Sorry, I did not understand that")
        return ""
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        speak("Sorry, I am having trouble accessing the Google Speech Recognition service right now")
        return ""


# speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

def get_weather(city):
    # enter your OpenWeatherMap API key here
    api_key = "4d756c29bb66df9af0a774974a789a85"

    # make a GET request to the OpenWeatherMap API to get the weather information of the city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    # check if the request was successful
    if response.status_code == 200:
        # parse the JSON response to get the temperature and weather description
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        # format the weather information as a string and speak it
        weather_info = f"The temperature in {city} is {temperature} degrees Celsius with {description}."
        print(weather_info)
        speak(weather_info)
    else:
        # if the request was unsuccessful, speak an error message
        error_message = "Sorry, there was an error retrieving the weather information. Please try again later."
        print(error_message)
        speak(error_message)


# Initialize GUI
root = tk.Tk()
root.title("Virtual Assistant")
root.iconbitmap("icon.ico")

# Set window size and position
window_width = 600
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Set window background color
root.config(bg="#000000")

# Create label for the text box
output_label = tk.Label(root, text="Conversation:", font=("Helvetica", 14), bg="#000000")
output_label.pack(pady=10)

# Create text box for the output
output = tk.Text(root, height=15, width=60, font=("Helvetica", 12))
output.pack(pady=10)

# Create a scrollbar for the text box
scrollbar = tk.Scrollbar(root, command=output.yview)
scrollbar.pack(side="right", fill="y")
output.config(yscrollcommand=scrollbar.set)

# Create a function to display messages in the text box
def display_message(message):
    output.insert("end-1c", message + "\n\n")
    output.see("end")

# Create label for the button
button_label = tk.Label(root, text="Click the button below and start talking to me.", font=("Helvetica", 14), bg="#000000")
button_label.pack(pady=20)

# define a function to handle the button click
def handle_click():
    with tqdm.tqdm(total=100, desc="Processing") as pbar:
        text = get_audio().lower()
        pbar.update(50)
        if text:
            display_message("You: " + text)

        if 'your name' in text:
            speak('I am Kushal, What can I do for you?')
            display_message("Assistant: I am Kushal, What can I do for you?")
        elif 'how are you' in text:
            print("I am amazing, how about you")
            speak('I am amazing, how about you')
            display_message("Assistant:I am amazing, how about you!")
        elif 'date' in text:
            date = datetime.datetime.now().strftime('%D/%M/%Y')
            print(date)
            speak("Today's Date" + date)
            display_message("Assistant: " +date)
        elif 'time' in text:
            time = datetime.datetime.now().strftime('%I:%M%p')
            print(time)
            speak('Current Time' + time)
            display_message("Assistant: " +time)
        elif 'weather' in text:
            # code for getting the weather information
            city = text.split(" ")[-1]  # get the last word in the text as the city name
            get_weather(city)
    
        elif 'news' in text:
            speak('Here are the top news headlines')
            url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=ebe690ff3dad44b1ba6959951fc49c70'
            response = requests.get(url)
            json_data = json.loads(response.text)
            articles = json_data['articles']
            for article in articles:
                speak(article['title'])
                display_message("Assistant: " +article['title'])

        elif 'youtube' in text:
            speak("Opening YouTube")
            url = f"https://www.youtube.com"
            webbrowser.get().open(url)
        elif 'wikipedia' in text:
            speak('searching wikipedia...')
            text = text.replace("wikipedia", "")
            results = wikipedia.summary(text, sentences =2)
            print(results)
            speak(results)
            display_message("Assistant: " +results)
        
        elif 'joke' in text:
            jokes=pyjokes.get_joke()
            speak(jokes)
            display_message("Assistant: " +jokes)
        elif 'calculate' in text:
            # code for performing calculations
            try:
                # extract the expression from the text
                expression = text.split('calculate')[-1]
                # evaluate the expression using Python's eval() function
                result = eval(expression)
                print(result)
                speak(f"The result is {result}")
                display_message("Assistant: " +result)
            except:
                error_message = "Sorry, I could not perform the calculation."
                print(error_message)
                speak(error_message)
                display_message("Assistant:Sorry, I could not perform the calculation.")
        elif 'bye' in text:
            speak("Goodbye, till next time")
            display_message("Goodbye, till next time") 
        
            root.quit()
        root.update()



# create a button to trigger the voice recognition
button = tk.Button(root, text="Start Listening", font=("Helvetica", 14), bg="#000000", fg="#000000", command=handle_click, pady=10)
button.pack()

# start the GUI
root.mainloop()