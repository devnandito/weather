from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from weather.users.models import User, Profile
from django.contrib.auth.forms import PasswordResetForm

# Python
import random, string

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'password1', 'password2', 'is_active')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active')

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('level', 'description', 'picture',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'level', 'description', 'picture',)

class CustomNewsCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
       super(CustomNewsCreationForm, self).__init__(*args, **kwargs)
       self.fields['password1'].widget.attrs['hidden'] = True
       self.fields['password2'].widget.attrs['hidden'] = True
       self.fields['password1'].widget.attrs['value'] = 'user12345678'
       self.fields['password2'].widget.attrs['value'] = 'user12345678'
       self.fields['is_active'].initial = False

    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'password1', 'password2', 'is_active')

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class CustomMetCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        gen_pwd = get_random_string(8)
        super(CustomMetCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['hidden'] = True
        self.fields['password2'].widget.attrs['hidden'] = True
        self.fields['password1'].widget.attrs['value'] = gen_pwd
        self.fields['password2'].widget.attrs['value'] = gen_pwd
        self.fields['is_active'].initial = True
    
    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'password1', 'password2', 'is_active')

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            msg = "El email no se encuentra registrado en el sistema."
            self.add_error('email', msg)
        return email

class FormUnsuscribed(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)

# class NewsletterForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#        super(NewsletterForm, self).__init__(*args, **kwargs)
#        self.fields['password1'].widget.attrs['hidden'] = True
#        self.fields['password2'].widget.attrs['hidden'] = True
#        self.fields['password1'].initial = 'user12345678'
#        self.fields['password2'].initial = 'user12345678'

#     email = forms.CharField(label='Email', max_length=100)
#     username = forms.CharField(label='Username', max_length=100)
#     first_name = forms.CharField(label='First name', max_length=100)
#     last_name = forms.CharField(label='Last name', max_length=100)
#     password1 = forms.CharField(label='Password1', max_length=100)
#     password2 = forms.CharField(label='Password2', max_length=100)