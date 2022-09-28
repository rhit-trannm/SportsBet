from django.shortcuts import render

from sportsstars.forms import LoginForm

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login(request):
    if(request.method=='POST'):
        #Form filled
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate login here
            logged_in = True
            if logged_in:
                #Login successful
                return render(request, 'home.html', {'username': form.cleaned_data['Username']})
            else:
                #Bad login
                return render(request, 'login.html', {'username': form.cleaned_data['Username']})
    else:
        #Return with empty form
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

