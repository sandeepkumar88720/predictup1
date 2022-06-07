from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}


class Charttwo(forms.Form):
    name = forms.CharField()
    style = forms.CharField()
    period = forms.CharField()
    interval = forms.CharField()
    type = forms.CharField()
    volume = forms.BooleanField()


class Predict(forms.Form):
    search = forms.CharField()
