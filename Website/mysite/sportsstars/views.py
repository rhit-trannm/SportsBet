from django.shortcuts import render
from sportsstars.forms import AcctForm, LoginForm
from datetime import datetime, timedelta, date
from Python import Redis



# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login(request):
    if(request.method=='POST'):
        #Form filled
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate login here
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logged_in = Redis.loginCheck(username, password)
            if logged_in:
                #Login successful
                return homeRender(request, username)
            else:
                #Bad login
                newForm = LoginForm(initial={'username': username})
                return render(request, 'login.html', {'form': newForm, 'error_message':'Incorrect Username/Password'})
    else:
        #Return with empty form
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def homeRender(request, username):
    balance = 0
    return render(request, 'home.html', {'username': username, 'balance': balance})


def acct(request):
    if(request.method=='POST'):
        form = AcctForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            birthday = form.cleaned_data['birthday']
            yr = date.today().year
            if birthday>date.today().replace(year=yr-21):
                newForm = AcctForm(initial={'name': name, 'birthday': birthday, 'username': username})
                return render(request, 'acct.html', {'form': newForm, 'error_message': 'Age must be at least 21'})
            try:
                Redis.CreateUser(name, username, password, birthday)
                newForm = LoginForm(initial={'username': username})
                return render(request, 'login.html', {'form': newForm})
            except ValueError:
                newForm = AcctForm(initial={'name': name, 'birthday': birthday})
                return render(request, 'acct.html', {'form':form, 'error_message':'Username already exists. Please use a different username'})
    else:
        form = AcctForm()
        return render(request, 'acct.html', {'form': form})


def stats(request):
    return render(request, 'stats.html', {})

def bets(request):
    return render(request, 'bets.html', {})
