from django.contrib import admin
from .models import Weather, HistoricalWeather

# Register your models here.
admin.site.register(Weather)
admin.site.register(HistoricalWeather)
