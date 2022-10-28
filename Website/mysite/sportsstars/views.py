from django.shortcuts import render
from sportsstars.forms import AcctForm, LoginForm, FriendForm
from datetime import datetime, timedelta, date
from Python import Redis, neo4j



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
            try:
                logged_in = neo4j.Login_Check(username, password)
            except:
                logged_in = neo4j.Login_Check(username, password)
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


def homeRender(request, username, msg=''):
    balance = neo4j.Get_Balance(username)
    num_Friends = neo4j.Get_Number_Of_Friends(username)
    form = FriendForm()
    return render(request, 'home.html', {'username': username, 'balance': balance, 'friends': num_Friends, 'form':form, 'msg':msg})

def friends(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.cleaned_data['friend']
            user = request.POST.get('username')
            friend_exists = neo4j.Find_User(friend)
            if friend_exists==0:
                return homeRender(request, user, f'user {friend} does not exist')
            else:
                if neo4j.Check_Friend(user, friend) == 1:
                    return homeRender(request, user, f'user {friend} is already your friend')
                neo4j.Add_Friend(user, friend)
                return homeRender(request, user, f'user {friend} added as friend')
    else:
        return login(request)

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
                #Redis.CreateUser(name, username, password, birthday)
                neo4j.Create_User(name, username, password, birthday)
                newForm = LoginForm(initial={'username':username})
                return render(request, 'login.html', {'form':newForm})
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