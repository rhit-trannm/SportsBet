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

class playerSearch(forms.Form):
    Name = forms.CharField(label='Name', max_length=50, required=False, empty_value=None)
    Team = forms.CharField(label = 'Team', max_length=40, required=False, empty_value=None)

class gameSearch(forms.Form):
    date = forms.DateField(label='date', widget=forms.SelectDateWidget(years=[2022]))


class betType(forms.Form):
    bet = forms.ChoiceField(label='bet', choices=[("O", "Over/Under"), ("M", "Money Line")])

class overUnder(forms.Form):
    over_under = forms.ChoiceField(label='over_under', choices=[(0, 'Over'), (1,'Under')])
    amount = forms.IntegerField(label='amount', min_value=1)

class moneyLine(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        super(moneyLine, self).__init__(*args, **kwargs)
        self.fields['winner'] = forms.ChoiceField(label='winner', choices=choices)
        self.fields['amount'] = forms.IntegerField(label='amount', min_value=1)

class balanceForm(forms.Form):
    type = forms.ChoiceField(label='type', choices=[('D', 'Deposit'), ('W', 'Withdraw')])
    amount = forms.IntegerField(label='amount', min_value=1)