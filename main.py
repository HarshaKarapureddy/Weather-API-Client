#IMPORTING DATETIME AND REQUESTS MODULES
import datetime as dt
import requests


#API KEY
Api_Key = '373ac139ad20b1a4b0180edd7653578e'


#FUNCTION TO CONVERT KELVIN
def kelvin_converter(kelvin):
    Celsius = kelvin - 273.15
    Fahrenhiet = Celsius * (9/5) + 32
    return Celsius, Fahrenhiet


#FUNCTION TO FIND GENERAL WIND DIRECTION
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


#CHOSEN LOCATION
location = 'Nashville'


#API CALL FOR GEOCODING API
location_url = 'http://api.openweathermap.org/geo/1.0/direct?'
url = location_url + "appid=" + Api_Key + "&q=" + location + '&limit='
geocoding_response = requests.get(url).json()


#API CALL FOR OPENWEATHER API
base_url = 'https://api.openweathermap.org/data/2.5/weather?'
url2 = base_url + "appid=" + Api_Key + "&lat=" + str(geocoding_response[0]['lat']) + '&lon=' + str(geocoding_response[0]['lon'])
openweather_response = requests.get(url2).json()


#DESIRED DATA PULLED FROM API RESPONSE
kelvin_Temp = openweather_response['main']['temp']
celsius_Temp, fahrenheit_Temp = kelvin_converter(kelvin_Temp)
humidity = openweather_response['main']['humidity']
wind_speed = openweather_response['wind']['speed']
wind_dir_ang = openweather_response['wind']['deg']
wind_gen_dir = deg_to_dir(wind_dir_ang)
description = openweather_response['weather'][0]['description']
dawn = dt.datetime.utcfromtimestamp(openweather_response['sys']['sunrise'] + openweather_response['timezone'])
dusk = dt.datetime.utcfromtimestamp(openweather_response['sys']['sunset'] + openweather_response['timezone'])


#SCREEN OUTPUT
print(f"The General Weather in {location}: {description}")
print(f"The temperature in {location}: {celsius_Temp:.2f}°C or {fahrenheit_Temp:.2f}°F")
print(f"The wind speed and direction in {location}: {wind_speed} m/s {wind_gen_dir}")
print(f"The humidity in {location}: {humidity}%")
print(f"The sun in {location} rises at {dawn} (local time)")
print(f"The sun in {location} sets at {dusk} (local time)")