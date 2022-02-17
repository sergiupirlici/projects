import requests
import json
from datetime import datetime

from plotly.graph_objs import bar
from plotly import offline

api_key = "ae9ea3be210391afd9352138f3259608"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

list_of_cities = ['baia mare', 'bistrița', 'cluj', 'târgu mureș', 'sighișoara', 'arad', 'pitești', 'oradea', 'botoșani',
                  'bucurești', 'târgoviște', 'craiova', 'galați', 'giurgiu', 'deva', 'slobozia', 'iași', 'buftea', 'slatina', 'ploiești']
localitati, temperaturi = [], []
max_temps_by_city = []

for city in list_of_cities:
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    
    lon = response.json()["coord"]["lon"]
    lat = response.json()["coord"]["lat"]

    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily&appid=ae9ea3be210391afd9352138f3259608&units=metric')
    # print(json.dumps(response.json(), indent=4))
    print(response.json().keys())
    
    first_24_hours = response.json()["hourly"][:24]
    # print(len(first_24_hours))

    max_temp = sorted(first_24_hours, key=lambda k: k['temp'])[-1]
    max_temps_by_city.append({
        "city": city,
        "timp": max_temp["dt"] + response.json()["timezone_offset"],
        "temp": max_temp["temp"]
    })

max_temps_by_city = sorted(
    max_temps_by_city, key=lambda k: k['temp'], reverse=True)
# print(max_temps_by_city)

for item in max_temps_by_city:
    hour = datetime.utcfromtimestamp(item["timp"]).strftime('%H')
    localitati.append(f'{item["city"]} ({hour}:00)')
    temperaturi.append(item["temp"])
    print(f'{item["city"]} > {item["temp"]} > {hour}:00')


data = [{'type': 'bar', 'x': localitati, 'y': (temperaturi), }]
my_layout = {'title': 'Temperaturi maxime pentru următoarele 24 de ore',
             'xaxis': {'title': 'Localități'}, 'yaxis': {'title': 'Temperatura, °C'}, }
fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='weather_repos.html')
