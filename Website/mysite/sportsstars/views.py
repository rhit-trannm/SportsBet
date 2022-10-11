from django.shortcuts import render
from sportsstars.forms import AcctForm, LoginForm
from Python.Redis import *

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login(request):
    if(request.method=='POST'):
        #Form filled
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate login here
            
            logged_in = False
            if logged_in:
                #Login successful
                return render(request, 'home.html', {'username': form.cleaned_data['username']})
            else:
                #Bad login
                newForm = LoginForm(initial={'username': form.cleaned_data['username']})
                return render(request, 'login.html', {'form': newForm, 'error_message':'Incorrect Username/Password'})
    else:
        #Return with empty form
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def acct(request):
    if(request.method=='POST'):
        form = AcctForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = AcctForm()
        return render(request, 'acct.html', {'form': form})