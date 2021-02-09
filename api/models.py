from django.db import models

# Create your models here.


class Weather(models.Model):
    name = models.CharField(max_length=255)
    main_description = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    temperature = models.FloatField(null=True)
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class HistoricalWeather(models.Model):
    name = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=500, null=True)
    temp_day = models.CharField(max_length=500, null=True)
    temp_night = models.CharField(max_length=500, null=True)
    sunrise = models.CharField(max_length=500, null=True)
    sunset = models.CharField(max_length=500, null=True)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
