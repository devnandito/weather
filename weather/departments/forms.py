from django import forms
from weather.departments.models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('nombre_dpto', 'nombre_cap')