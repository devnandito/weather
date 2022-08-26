from django import forms
from weather.stationtypes.models import StationType

class StationTypeForm(forms.ModelForm):
    class Meta:
        model = StationType
        fields = ('nombre',)