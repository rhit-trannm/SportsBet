from django.shortcuts import render
from sportsstars.forms import AcctForm, LoginForm, FriendForm, playerSearch
from datetime import datetime, timedelta, date
from Python import Redis, neo4j, middlelayer, RavenDB
from Python.middlelayer import Logging
import redis
import py2neo


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
                logged_in = Redis.LoginCheck(username, password)
            except redis.exceptions.ConnectionError:
                logged_in = neo4j.Login_Check(username, password)
            except py2neo.ClientError:
                logged_in = RavenDB.LoginCheck(username, password)
            except:
                newForm = LoginForm(initial={'username':username})
                return render(request, 'login.html', {'form':newForm, 'error_message': 'Login is unavailable at this time.'})
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
    try:
        balance = neo4j.Get_Balance(username)
    except:
        balance = 'UNAVAILABLE'
    try:
        num_Friends = neo4j.Get_Number_Of_Friends(username)
    except:
        num_Friends = 'UNAVAILABLE'
    form = FriendForm()
    return render(request, 'home.html', {'username': username, 'balance': balance, 'friends': num_Friends, 'form':form, 'msg':msg})

def friends(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.cleaned_data['friend']
            user = request.POST.get('username')
            try:
                friend_exists = neo4j.Find_User(friend)
                if friend_exists==0:
                    return homeRender(request, user, f'user {friend} does not exist')
            except:
                pass

            else:
                try:
                    if neo4j.Check_Friend(user, friend) == 1:
                        return homeRender(request, user, f'user {friend} is already your friend')
                except:
                    pass
                Friend = middlelayer.Friends(user, friend)
                middlelayer.Logging('CREATE', Friend)
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
                obj = middlelayer.User(name, username, password, birthday.strftime("%d-%m-%Y"), 1000)
                Logging("CREATE", obj)
                newForm = LoginForm(initial={'username':username})
                return render(request, 'login.html', {'form':newForm})
            except ValueError:
                newForm = AcctForm(initial={'name': name, 'birthday': birthday})
                return render(request, 'acct.html', {'form':form, 'error_message':'Username already exists. Please use a different username'})
    else:
        form = AcctForm()
        return render(request, 'acct.html', {'form': form})

def players(request):
    if request.method == 'POST':
        form = playerSearch(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            team = form.cleaned_data['Team']
            if name is not None and team is None:
                players = RavenDB.SearchPlayerName(name)
            if name is None and team is not None:
                players = RavenDB.SearchPlayerTeam(team)
            if name is not None and team is not None:
                players = RavenDB.SearchPlayerNameTeam(name, team)
            if name is None and team is None:
                players = RavenDB.SearchPlayers()
            if players is None:
                results = []
            else:
                results = [p.__dict__ for p in players]
            newForm = playerSearch()
            return render(request, "stats.html", {'form':form, 'players':results})
        return render(request, "stats.html", {'error':form.errors})
    form = playerSearch()
    return render(request, "stats.html", {'form': form})

def playerstats(request):
    if request.method == 'POST':
        player = request.POST['submit']
        games = RavenDB.QueryPlayerGames(player)
        print(len(games))
        results = [g.__dict__ for g in games]
        return render(request, "playerstats.html", {'games':results})
    return render(request, 'home.html', {})

def stats(request):
    return render(request, 'stats.html', {})

def bets(request):
    return render(request, 'bets.html', {})