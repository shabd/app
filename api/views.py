from django.shortcuts import render
from .models import Weather, HistoricalWeather
from .forms import CityForm
import requests
from django.shortcuts import get_object_or_404, render
from django.forms.models import model_to_dict
from .serializer import WeatherSerializer, HistoricalWeatherSerializer

API_KEY = '09cd8d19b555555ca9a4b86ba933f327'
Map_BOX_API = 'pk.eyJ1Ijoic2hhYmQiLCJhIjoiY2trdnAwdWN6MGNzNjJubzRsZmgybnJoaSJ9.NxBM3PXS0qB3CBt7zKiYCg'


# def weather(request):
#     weather = ''
#     form = CityForm()
#     if request.method == 'POST':
#         filled_form = CityForm(request.POST)
#         if filled_form.is_valid():

#             weather = Weather()
#             # get address from form
#             current_city = filled_form.cleaned_data['city_name']
#             #  need lat and long
#             response = requests.get(
#                 f'http://api.mapbox.com/geocoding/v5/mapbox.places/{current_city}.json?access_token={Map_BOX_API}')
#             json = response.json()
#             weather.lat = json['features'][0]['geometry']['coordinates'][0]
#             weather.lng = json['features'][0]['geometry']['coordinates'][1]
#             # pass lat and long to openweather and get city name <API CALL to OPENWEATHER >
#             weather_response = requests.get(
#                 f'https://api.openweathermap.org/data/2.5/onecall?lat={weather.lat}&lon={weather.lng}&exclude=alerts,hourly,minutely&appid={API_KEY}')
#             weather_json = weather_response.json()
#             # Save input as Weather and History name fields as OneAPI doesnt provide it
#             weather.name = current_city

#             weather.main_description = weather_json['current']['weather'][0]['main']
#             weather.temperature = weather_json['current']['temp']
#             weather.description = weather_json['current']['weather'][0]['description']
#             weather.feels_like = weather_json['current']['feels_like']
#             weather.wind_speed = weather_json['current']['wind_speed']
#             weather.save()

#     return render(request, 'weather/weather.html', {'form': form, 'weather': weather})

def weather(request):
    weather = ''
    queryset = ''
    if request.method == 'POST':
        name = request.POST['name']
        print(f'NAME FROM WEAATHER CALL {name}')
        # make api call to map box
        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={Map_BOX_API}')
        json = response.json()
        # get lat and lng
        weather = Weather()
        weather.name = name
        weather.lat = json['features'][0]['geometry']['coordinates'][0]
        weather.lng = json['features'][0]['geometry']['coordinates'][1]
        #  make api call to open weather
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat={weather.lat}&lon={weather.lng}&appid={API_KEY}')
        r = weather_response.json()
        weather.main_description = r['weather'][0]['main']
        weather.temperature = r['main']['temp']
        weather.description = r['weather'][0]['description']
        weather.max_temp = r['main']['temp_max']
        weather.min_temp = r['main']['temp_min']
        weather.save()
        serializer_class = WeatherSerializer

    return render(request, 'weather/weather.html', {
        'weather': weather})


def historical_weather(request):

    if request.method == 'POST':
        name = request.POST['name']
        print(f"NAME FROM HISTORICAL WEATHER {name}")
        data = HistoricalWeather()
        # Make call to  map box
        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={Map_BOX_API}')
        json = response.json()
        lat = json['features'][0]['geometry']['coordinates'][0]
        lng = json['features'][0]['geometry']['coordinates'][1]
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&exclude=alerts,hourly,minutely&appid={API_KEY}')
        weather_json = weather_response.json()
        data.time = weather_json['daily'][0]['dt']
        data.temp_day = weather_json['daily'][0]['temp']['day']
        data.temp_night = weather_json['daily'][0]['temp']['night']
        data.sunrise = weather_json['daily'][0]['sunrise']
        data.sunset = weather_json['daily'][0]['sunset']
        data.save()
    return render(request, 'weather/historical_weather.html')
