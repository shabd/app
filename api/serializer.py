from rest_framework import serializers
from .models import Weather, HistoricalWeather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class HistoricalWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalWeather
        fields = '__all__'
