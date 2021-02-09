from django import forms
from .views import *


class CityForm(forms.Form):
    city_name = forms.CharField()
