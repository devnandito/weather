from django import forms
from weather.stations.models import Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ('name', 'location', 'fktypestation')