#Importing required modules
import datetime as dt
import requests
from customtkinter import *

#Initialization of root window
app = CTk()
app.title("Weather API")
app.geometry('1000x500')
app.config(bg="#390099")
app.resizable(0,0)

#Title-Entry-Frame Initialization
Title_Entry_Frame = CTkFrame(master=app, fg_color="#9E0059", width=500, height=510, bg_color="#390099",
                             corner_radius=False)
Title_Entry_Frame.grid(row=0, column=0)
Title_Entry_Frame.grid_propagate(False)

#Output-Frame Initialization
Output_Frame = CTkFrame(master=app, fg_color="#390099", width=500, height=510, bg_color="#390099",
                             corner_radius=False)
Output_Frame.grid(row=0, column=1)
Output_Frame.grid_propagate(False)

#Output-Title
Output_Title = CTkLabel(master=Output_Frame, text="Location's Current Weather", text_color="#FF0054",
                       font=("Roboto", 37, "bold"), bg_color="#390099", corner_radius=10,
                        fg_color="#9E0059")
Output_Title.grid(row=0, column=0, padx=(10,15), pady=10, sticky='we', columnspan=2)

#Output-Text
Output_Text = CTkLabel(master=Output_Frame, text_color="#FF0054", text="",
                       font=("Roboto", 20, "bold"), bg_color="#390099", justify="left")
Output_Text.grid(row=1, column=0, padx=10, pady=10 ,sticky='w', columnspan=3)

#Title
Title_Label = CTkLabel(master=Title_Entry_Frame, text="Weather API", text_color="#FF5400",
                       font=("Roboto", 60, "bold"), bg_color="#9E0059", corner_radius=10, fg_color="#390099")
Title_Label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')

#Credit Subtitile
Prompt_Label = CTkLabel(master=Title_Entry_Frame, text="By Harsha Karapureddy", text_color="#FF5400",
                       font=("Roboto", 15, "bold"), bg_color="#9E0059")
Prompt_Label.grid(row=1, column=0, padx=(20,0), pady=(0,100) ,sticky='nw')

#User-Prompt
Prompt_Label = CTkLabel(master=Title_Entry_Frame, text="Please enter a city name", text_color="#FF5400",
                       font=("Roboto", 20, "bold"), bg_color="#9E0059", corner_radius=10, fg_color="#390099")
Prompt_Label.grid(row=3, column=0, padx=(125,0), pady=(10,0), sticky='w')

#Location Entry
location = StringVar()  #Chosen location
Location_Entry = CTkEntry(master=Title_Entry_Frame, width=255, textvariable= location)
Location_Entry.grid(row=4, column=0, columnspan = 3, padx=(125,0), pady=(10,0), sticky='w')

#Function for API call
def api_call():
    try:
        location_url = 'http://api.openweathermap.org/geo/1.0/direct?'
        url = location_url + "appid=" + Api_Key + "&q=" + location.get() + '&limit='
        geocoding_response = requests.get(url, timeout=10).json()

        base_url = 'https://api.openweathermap.org/data/2.5/weather?'
        url2 = base_url + "appid=" + Api_Key + "&lat=" + str(geocoding_response[0]['lat']) + '&lon=' + str(
            geocoding_response[0]['lon'])
        openweather_response = requests.get(url2, timeout=10).json()

        kelvin_Temp = openweather_response['main']['temp']
        celsius_Temp, fahrenheit_Temp = kelvin_converter(kelvin_Temp)
        humidity = openweather_response['main']['humidity']
        wind_speed = openweather_response['wind']['speed']
        wind_dir_ang = openweather_response['wind']['deg']
        wind_gen_dir = deg_to_dir(wind_dir_ang)
        description = openweather_response['weather'][0]['description']
        dawn = dt.datetime.fromtimestamp(openweather_response['sys']['sunrise'] + openweather_response['timezone'],
                                         dt.timezone.utc)
        dusk = dt.datetime.fromtimestamp(openweather_response['sys']['sunset'] + openweather_response['timezone'],
                                         dt.timezone.utc)

        Output_Text.configure(text=f"The General Weather in {location.get()}:\n{description.capitalize()}\n"
                                "\n"f"The temperature in {location.get()}:\n{celsius_Temp:.2f}°C or {fahrenheit_Temp:.2f}°F\n"
                                "\n"f"The wind speed and direction in {location.get()}:\n{wind_speed} m/s {wind_gen_dir}\n"
                                "\n"f"The humidity in {location.get()}:\n{humidity}%\n"
                                "\n"f"The sun in {location.get()} rises at:\n{dawn} (local time)\n"
                                "\n"f"The sun in {location.get()} sets at:\n{dusk} (local time)")
    except Exception:
        Output_Text.configure(text="The city you entered does not exist.\nTry again.")



#Submit_Button
submit_Button = CTkButton(master=Title_Entry_Frame, text="Submit", text_color="#FF5400",
                       font=("Roboto", 15, "bold"), fg_color="#390099", command=api_call)
submit_Button.grid(row=5, column=0,padx=(180,0), pady=(10,0), sticky='w')


#API key
Api_Key = open('API_KEY', 'r').read() #Get your own API key from OpenWeather website

#Fucntiont to convert kelvin
def kelvin_converter(kelvin):
    Celsius = kelvin - 273.15
    Fahrenhiet = Celsius * (9/5) + 32
    return Celsius, Fahrenhiet


#Function to find general wind direction
def deg_to_dir(deg):
    direction = "None"
    if(deg == 0):
        direction = "North"
    elif(0<deg<90):
        direction = "Northeast"
    elif(deg == 90):
        direction = "East"
    elif(90<deg<180):
        direction = "Southeast"
    elif(deg == 180):
        direction = "South"
    elif(180<deg<270):
        direction = "Southwest"
    elif(deg == 270):
        direction = "West"
    elif(270<deg<360):
        direction = "Northwest"
    elif(deg == 360):
        direction = "North"
    else:
        direction = "Unknown"

    return direction

app.mainloop()
