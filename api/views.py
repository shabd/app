from django.shortcuts import render
from .models import Weather, HistoricalWeather, ApiKey
import requests
from django.shortcuts import get_object_or_404, render
from django.core import serializers


def weather(request):
    if request.method == 'POST':
        api = ApiKey()
        map_box_api = ApiKey.objects.get(name='map_box_api')
        apikey = map_box_api.value
        name = request.POST['name']
        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={apikey}')
        json = response.json()

        weather = Weather()
        weather.name = name
        weather.lat = json['features'][0]['geometry']['coordinates'][0]
        weather.lng = json['features'][0]['geometry']['coordinates'][1]
        open_weather = ApiKey.objects.get(name='open_weather')
        open_weather_api = open_weather.value
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat={weather.lat}&lon={weather.lng}&appid={open_weather_api}')
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
        api = ApiKey()
        map_box_api = ApiKey.objects.get(name='map_box_api')
        apikey = map_box_api.value
        response = requests.get(
            f'http://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json?access_token={apikey}')
        json = response.json()
        lat = json['features'][0]['geometry']['coordinates'][0]
        lng = json['features'][0]['geometry']['coordinates'][1]
        open_weather = ApiKey.objects.get(name='open_weather')
        open_weather_api = open_weather.value
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&exclude=alerts,hourly,minutely&appid={open_weather_api}')
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
