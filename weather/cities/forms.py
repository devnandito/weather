from django import forms
from weather.cities.models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('id_dpto', 'nombre',)