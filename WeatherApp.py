from dotenv import load_dotenv
import requests
import os
from tkinter import *
import customtkinter
from customtkinter import CTkImage
from PIL import Image, ImageTk
from io import BytesIO

script_dir = os.path.dirname(__file__) # Extracts direcotry of current file
os.chdir(script_dir) # Changes current dir to working directory
load_dotenv(dotenv_path='WEATHER_API_KEY.env') # Loads env file
api_key = os.getenv('WEATHER_API_KEY') # Get value of api key

def load_icon(url, size=(40, 40)): # Gets the image from the url, gets the image from the response and loads it - weather_icon
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))  
    return CTkImage(light_image=img, size=size)

is_fahrenheit = True 
is_miles = True 

def toggle_temp_unit(): # Switches between farenheit and celcius
    global is_fahrenheit
    is_fahrenheit = not is_fahrenheit
    get_weather()

def toggle_distance_unit(): # Switches between miles and kilometers
    global is_miles
    is_miles = not is_miles
    get_weather()    

def get_weather():
    location = locationEntry.get()  # Retrieves location entered by user
    params = { # Parameters for the API request
        'key': api_key,
        'q': location
    }

    try:
        response = requests.get('https://api.weatherapi.com/v1/current.json', params=params) # Makes the API request

        if response.status_code == 200: # If response code indicates a successful request
            data = response.json() # Parse JSON response

            temp_f = data['current']['temp_f'] # Extracts all weather information needed
            feelslike_f = data['current']['feelslike_f']
            condition_text = data['current']['condition']['text']
            wind_mph = data['current']['wind_mph']
            wind_kph = data['current']['wind_kph']
            humidity = data['current']['humidity']
            cloud = data['current']['cloud']
            vis_miles = data['current']['vis_miles']
            vis_km = data['current']['vis_km']
            icon_url = "https:" + data['current']['condition']['icon']
            temp_c = data['current']['temp_c']
            feelslike_c = data['current']['feelslike_c']


            icon_url = "https:" + data['current']['condition']['icon'] # Loads the 'main icon' for weather_icon
            weather_icon = load_icon(icon_url, size=(100, 100))
            
            display_temp_label.configure(text=f"Current temperature in {location}: {temp_f}°f") # Updates UI with info
            feelslike_label.configure(text=f"Feels like: {feelslike_f}°f")
            condition_label.configure(text=f"Condition: {condition_text}")
            windspeed_label.configure(text=f"Windspeed: {wind_mph} MPH")
            humidity_label.configure(text=f"Humidity: {humidity}%")
            cloudcover_label.configure(text=f"Cloud cover: {cloud}%")
            visibility_label.configure(text=f"Visibility: {vis_miles} miles")

            weather_icon_label.configure(image=weather_icon) # Updates UI with image
            weather_icon_label.image = weather_icon 
            
        else:
            print(f"Error: {response.status_code} - {response.text}") # Returns response code and text if not 200

    except Exception as e: # Catches exceptions
        print(f"Error: {e}")        

    if not is_fahrenheit: # Swaps fahrenheit and celsius
        display_temp_label.configure(text=f"Current temperature in {location}: {temp_c:.1f}°C")
        feelslike_label.configure(text=f"Feels like: {feelslike_c:.1f}°C")
    else:
        display_temp_label.configure(text=f"Current temperature in {location}: {temp_f}°F")
        feelslike_label.configure(text=f"Feels like: {feelslike_f}°F")

    if not is_miles: # Swaps miles and kilometers
                windspeed_label.configure(text=f"Windspeed: {wind_kph:.1f} KPH")
                visibility_label.configure(text=f"Visibility: {vis_km:.1f} KM")
    else:
        windspeed_label.configure(text=f"Windspeed: {wind_mph:.1f} MPH")
        visibility_label.configure(text=f"Visibility: {vis_miles:.1f} miles")    


window = customtkinter.CTk()
window.geometry("480x750")
window.resizable(False, False)
window.title("Weather App")

icons = [] # Stores images of icons loaded

feelslike_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/116.png', size=(40, 40)) # Calls load_icon to load each specific icon
icons.append(feelslike_icon)

condition_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/119.png', size=(40, 40))
icons.append(condition_icon)

windspeed_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/122.png', size=(40, 40))
icons.append(windspeed_icon)

humidity_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/143.png', size=(40, 40))
icons.append(humidity_icon)

cloudcover_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/176.png', size=(40, 40))
icons.append(cloudcover_icon)

visibility_icon = load_icon('https://cdn.weatherapi.com/weather/64x64/day/179.png', size=(40, 40))
icons.append(visibility_icon)

locationEntry = customtkinter.CTkEntry(window, font=("Arial", 14))
locationEntry.place(x=240, y=250, anchor="center")

get_weather_button = customtkinter.CTkButton(window, text="Get Weather", command=get_weather)
get_weather_button.place(x=240, y=300, anchor="center")

weather_icon_label = customtkinter.CTkLabel(window,text="")
weather_icon_label.place(x=240, y=135, anchor="center")

display_temp_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18),text="")
display_temp_label.place(x=240, y=70, anchor="center",)

feelslike_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=feelslike_icon, compound='left',text="")
feelslike_label.place(x=240, y=390, anchor="center",)

condition_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=condition_icon, compound='left',text="")
condition_label.place(x=240, y=440, anchor="center",)

windspeed_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=windspeed_icon, compound='left',text="")
windspeed_label.place(x=240, y=490, anchor="center",)

humidity_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=humidity_icon, compound='left',text="")
humidity_label.place(x=240, y=540, anchor="center",)

cloudcover_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=cloudcover_icon, compound='left',text="")
cloudcover_label.place(x=240, y=590, anchor="center",)

visibility_label = customtkinter.CTkLabel(window,font=("Bahnschrift",18), image=visibility_icon, compound='left',text="")
visibility_label.place(x=240, y=640, anchor="center",)

toggle_temp_button = customtkinter.CTkButton(window, text="°F/°C", command=toggle_temp_unit)
toggle_temp_button.place(x=400, y=300, anchor="center")

toggle_distance_button = customtkinter.CTkButton(window, text="Miles/KM", command=toggle_distance_unit)
toggle_distance_button.place(x=80, y=300, anchor="center")

window.mainloop()