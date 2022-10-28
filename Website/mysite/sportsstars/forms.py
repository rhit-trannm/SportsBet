from django import forms
from datetime import datetime

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AcctForm(forms.Form):
    years = [i for i in range(1900, datetime.now().year+1)]
    name = forms.CharField(label='Name', max_length=25)
    birthday = forms.DateField(label='Birthday', widget=forms.SelectDateWidget(years=years))
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class FriendForm(forms.Form):
    friend = forms.CharField(label='friend', max_length=20)