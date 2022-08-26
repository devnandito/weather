from django import forms
from weather.locations.models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('__all__')