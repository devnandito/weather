from django import forms
from weather.forecasts.models import Forecast
from weather.cities.models import City

class FormForecast(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(FormForecast, self).__init__(*args, **kwargs)
       self.fields['user'].widget.attrs['hidden'] = True

    class Meta:
        model = Forecast
        fields = ('city', 'temperature', 'feels_like', 'wind', 'pressure', 'humidity', 'comment', 'user')
    

class FormAlert(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(FormAlert, self).__init__(*args, **kwargs)
       self.fields['user'].widget.attrs['hidden'] = True
    
    class Meta:
        model = Forecast
        fields = ('city', 'temperature', 'feels_like', 'pressure', 'humidity', 'comment', 'sender_name', 'alerts', 'events', 'start', 'end', 'user')
    
class FormPredict(forms.ModelForm):
    class Meta:
        model = Forecast
        fields = ('temperature', 'humidity', 'pressure',)


CITY = []
object_list = City.objects.all().order_by('nombre')
for item in object_list:
    CITY.append((item.nombre, item.nombre))
# CITY = (
#     ('Asunción','Asunción'),
#     ('Encarnación','Encarnación'),
#     ('Fernando de la Mora','Fernando de la Mora'),
#     ('Concepción','Concepción'),
#     ('San Pedro','San Pedro'),
#     )

class FormSearchCity(forms.Form):
    city = forms.ChoiceField(choices=CITY, widget=forms.Select, error_messages={'required': 'Este campo es obligatorio'})

class FormGeo(forms.Form):
    city = forms.CharField(label='Country', max_length=100)
    lat = forms.CharField(label='Lat', max_length=100)
    lon = forms.CharField(label='Lon', max_length=100)

# class FormForecast(forms.Form):
#     city = forms.CharField(label='City', max_length=100)
#     temperature = forms.CharField(label='Temperature', max_length=100)
#     feels_like = forms.CharField(label='Feels_like', max_length=100)
#     wind = forms.CharField(label='Wind', max_length=100)
#     pressure = forms.CharField(label='Pressure', max_length=100)
#     humidity = forms.CharField(label='Humidity', max_length=100)
#     comment = forms.CharField(label='Comment', max_length=100)

# class FormAlert(forms.Form):
#     city = forms.CharField(label='City', max_length=100)
#     temperature = forms.CharField(label='Temperature', max_length=100)
#     feels_like = forms.CharField(label='Feels_like', max_length=100)
#     wind = forms.CharField(label='Wind', max_length=100)
#     pressure = forms.CharField(label='Pressure', max_length=100)
#     humidity = forms.CharField(label='Humidity', max_length=100)
#     comment = forms.CharField(label='Comment', max_length=100)
#     sender_name = forms.CharField(label='Sender', max_length=100)
#     alerts = forms.CharField(label='Alerts', max_length=100)
#     events = forms.CharField(label='Events', max_length=100)