import os
import webbrowser
from modules.text_to_speech import speak
from datetime import datetime
import requests
from modules.spotify import play_song, pause_song, resume_song, stop_song, set_volume, increase_volume, decrease_volume, is_music_playing




def get_weather(city):
    api_key = "68d5aed6da829ea9b985160c33006378"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    
    if response.get("cod") != 200:
        return "City not found!"
    weather = response['weather'][0]['description']
    temp = response['main']['temp']
    return f"The weather in {city} is {weather} with a temperature of {temp}°C."

def search_web(command):
    """Search the web for the given query."""
    search_query = command.replace("search for", "").strip()
    if search_query:
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query} on the web.")
    else:
        speak("Please provide something to search for.")

def open_application(command):
    """Open commonly used applications based on the command."""
    if "chrome" in command:
        os.system("start chrome")
        speak("Opening Chrome.")
    elif "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad.")
    elif "calculator" in command:
        os.system("calc")
        speak("Opening Calculator.")
    else:
        speak("Sorry, I can't open that application right now.")

def get_time():
    """Get the current time."""
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def process_command(command):
    command = command.lower()  # Make command case-insensitive
    """Process the recognized command and respond."""
    if "time" in command:
        get_time()

    elif "search for" in command:
        search_web(command)

    elif "open" in command:
        open_application(command)
        
    elif "weather" in command:
        # Extract city from the command, if provided
        city = "pune"  # Default city
        words = command.split()
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = words[city_index]

        # Fetch and speak the weather
        weather_info = get_weather(city)
        speak(weather_info)
        
    elif "start" in command:
        song = command.replace("start", "").strip()
        if song:
            response = play_song(song)
            speak(response)
        else:
            speak("Please specify the song to play.")

        
    elif "pause" in command:
        response = pause_song()
        speak(response)

    elif "resume" in command:
        response = resume_song()
        speak(response)
        
    elif "stop" in command:
        response = stop_song()
        speak(response)
        
    elif "set volume" in command:
        volume = int(command.split("to")[-1].strip().replace('%', ''))
        set_volume(volume)
    elif "increased volume" in command:
        increase_volume()
    elif "decrees volume" in command:
        decrease_volume()
    elif "mute" in command:
        set_volume(0)
    
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        return False  # Signal to exit the assistant

    else:
        # Add polite and concise fallback
        speak("I'm not sure I can do that yet. Please try something else.")
    
    return True  # Ensure the assistant waits for new command after one is processed
