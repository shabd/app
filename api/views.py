from django.shortcuts import render
from .models import Weather, HistoricalWeather
import requests
from django.shortcuts import get_object_or_404, render
from django.core import serializers


API_KEY = '09cd8d19b555555ca9a4b86ba933f327'
Map_BOX_API = 'pk.eyJ1Ijoic2hhYmQiLCJhIjoiY2trdnAwdWN6MGNzNjJubzRsZmgybnJoaSJ9.NxBM3PXS0qB3CBt7zKiYCg'


def weather(request):
    if request.method == 'POST':
        name = request.POST['name']

        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={Map_BOX_API}')
        json = response.json()

        weather = Weather()
        weather.name = name
        weather.lat = json['features'][0]['geometry']['coordinates'][0]
        weather.lng = json['features'][0]['geometry']['coordinates'][1]

        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat={weather.lat}&lon={weather.lng}&appid={API_KEY}')
        r = weather_response.json()
        weather.main_description = r['weather'][0]['main']
        weather.temperature = r['main']['temp']
        weather.description = r['weather'][0]['description']
        weather.max_temp = r['main']['temp_max']
        weather.min_temp = r['main']['temp_min']
        weather.save()
        data = serializers.serialize('json', Weather.objects.all())

        return render(request, 'weather/weather.html', {'data': data})
    else:
        return render(request, 'weather/weather.html')


def historical_weather(request):

    if request.method == 'POST':
        name = request.POST['name']
        data = HistoricalWeather()
        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={Map_BOX_API}')
        json = response.json()
        lat = json['features'][0]['geometry']['coordinates'][0]
        lng = json['features'][0]['geometry']['coordinates'][1]
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&exclude=alerts,hourly,minutely&appid={API_KEY}')
        weather_json = weather_response.json()
        data.name = name
        data.time = weather_json['daily'][0]['dt']
        data.temp_day = weather_json['daily'][0]['temp']['day']
        data.temp_night = weather_json['daily'][0]['temp']['night']
        data.sunrise = weather_json['daily'][0]['sunrise']
        data.sunset = weather_json['daily'][0]['sunset']
        data.save()

        return render(request, 'weather/historical_weather.html', {'data': data})
    else:
        return render(request, 'weather/historical_weather.html',)
