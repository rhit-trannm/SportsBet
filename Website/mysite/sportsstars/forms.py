from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AcctForm(forms.Form):
    name = forms.CharField(label='Name', max_length=25)
    birthday = forms.DateField(label='Birthday')
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)