from django import forms
from weather.climatologies.models import Climatology

class ClimatologyForm(forms.ModelForm):
    class Meta:
        model = Climatology
        fields = '__all__'