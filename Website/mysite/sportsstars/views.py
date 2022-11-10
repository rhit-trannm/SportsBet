from django.shortcuts import render
from sportsstars.forms import AcctForm, LoginForm, FriendForm, playerSearch, gameSearch, betType, overUnder, moneyLine, balanceForm
from datetime import datetime, timedelta, date
from Python import Redis, neo4j, middlelayer, RavenDB
from Python.middlelayer import Logging
import redis
import py2neo


# Create your views here.
def home(request):
    user = request.GET['user']
    return homeRender(request=request, username=user)

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
            except:
                try:
                    logged_in = neo4j.Login_Check(username, password)
                except:
                    try:
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
                obj = RavenDB.User(username=username, password=password, name=name, birthday=birthday.strftime("%d-%m-%Y"), balance=1000)
                Logging("CREATE", obj)
                newForm = LoginForm(initial={'username':username})
                return render(request, 'login.html', {'form':newForm})
            except ValueError:
                newForm = AcctForm(initial={'name': name, 'birthday': birthday})
                return render(request, 'acct.html', {'form':form, 'error_message':'Username already exists. Please use a different username'})
    else:
        form = AcctForm()
        return render(request, 'acct.html', {'form': form})

def wallet(request):
    if request.method == 'POST':
        form = balanceForm(request.POST)
        user = request.POST['user']
        if form.is_valid():
            type = form.cleaned_data['type']
            amount = form.cleaned_data['amount']
            if type == 'W':
                try:
                    balance = neo4j.Get_Balance(user)
                    if balance < amount:
                        newForm = balanceForm(initial=form.cleaned_data)
                        return render(request, "wallet.html", {'form':newForm, 'user':user, 'msg':f'Not enough balance to withdraw. {amount} available.', 'balance':balance})
                except:
                    pass
                middlelayer.Logging("UPDATE", middlelayer.Balance(user, -1*amount))
                try:
                    new_bal = neo4j.Get_Balance(user)
                except:
                    new_bal = ''
                newForm = balanceForm()
                return render(request, "wallet.html", {'form':newForm, 'user':user, 'msg':f'{amount} withdrawn.', 'balance':new_bal})
            if type == 'D':
                middlelayer.Logging("UPDATE", middlelayer.Balance(user, amount))
                try:
                    new_bal = neo4j.Get_Balance(user)
                except:
                    new_bal = ''
                newForm = balanceForm()
                return render(request, "wallet.html", {'form':newForm, 'user':user, 'msg':f'{amount} deposited.', 'balance':new_bal})
    form = balanceForm()
    user = request.GET['user']
    try:
        new_bal = neo4j.Get_Balance(user)
    except:
        new_bal = ''
    return render(request, "wallet.html", {'form':form, 'user':user, 'balance':new_bal})

def players(request):
    if request.method == 'POST':
        form = playerSearch(request.POST)
        user = request.POST['user']
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
            return render(request, "stats.html", {'form':form, 'players':results, 'user':user})
        return render(request, "stats.html", {'error':form.errors, 'user': user})
    user = request.GET['user']
    form = playerSearch()
    return render(request, "stats.html", {'form': form, 'user':user})

def playerstats(request):
    if request.method == 'POST':
        player = request.POST['player']
        user = request.POST['user']
        games = RavenDB.QueryPlayerGames(player)
        print(len(games))
        results = [g.__dict__ for g in games]
        return render(request, "playerstats.html", {'games':results, 'user':user})
    return render(request, 'home.html', {})


def games(request):
    if request.method == 'POST':
        form = gameSearch(request.POST)
        user = request.POST['user']
        if form.is_valid():
            date = form.cleaned_data['date']
            games = RavenDB.GetMatches(date.strftime("%Y-%m-%d"))
            results = [g.__dict__ for g in games]
            for g in results:
                temp_home = RavenDB.QueryTeam(g['homeTeamId'])
                g['home_team'] = temp_home.full_name
                temp_away = RavenDB.QueryTeam(g['awayTeamID'])
                g['away_team'] = temp_away.full_name
                if g['winningTeamID'] is not None:
                    if g['winningTeamID'] == g['homeTeamId']:
                        g['Result'] = temp_home.abbreviation + ' win'
                    else:
                        g['Result'] = temp_away.abbreviation + 'win'
            newForm = gameSearch(initial={'date':datetime.today()})
            return render(request, "games.html", {'games': results, 'user': user, 'form':newForm})
    user = request.GET['user']
    form = gameSearch(initial={'date':datetime.today()})
    return render(request, "games.html", {'form':form, 'user':user})

def teamstats(request):
    if request.method == 'POST':
        user = request.POST['user']
        home_team = request.POST['home']
        away_team = request.POST['away']
        game = request.POST['match']
        date = request.POST['date']
        home_season = RavenDB.GetSeason(home_team)
        away_season = RavenDB.GetSeason(away_team)
        seasons = [home_season, away_season]
        home_name = home_season.TEAM_NAME
        away_name = away_season.TEAM_NAME
        form = betType()
        return render(request, "teamstats.html", {'stats':seasons, 'home_name': home_name, 'away_name':away_name, 'user':user, 'game':game, 'date':date, 'form':form, 'home':home_team, 'away': away_team})

def bets(request):
    if request.method == 'POST':
        form = betType(request.POST)
        if form.is_valid():
            user = request.POST['user']
            home_team = request.POST['home']
            away_team = request.POST['away']
            home_name = request.POST['homename']
            away_name = request.POST['awayname']
            game = request.POST['match']
            bet_type = form.cleaned_data['bet']
            if bet_type == 'O':
                newForm = overUnder()
                return render(request, "bets.html", {'form':newForm, 'user':user, 'home':home_team, 'away':away_team, 'game':game, 'type':bet_type})
            elif bet_type == 'M':
                newForm = moneyLine(choices = [(home_team, home_name), (away_team, away_name)])
                return render(request, "bets.html", {'form':newForm, 'user':user, 'home':home_team, 'home_name':home_name, 'away':away_team, 'away_name':away_name, 'game':game, 'type':bet_type})
        return render(request, "home.html", {'msg':form.errors})


def placeBet(request):
    if request.method == 'POST':
        bet_type = request.POST['type']
        user = request.POST['user']
        game = request.POST['game']
        home_team = request.POST['home']
        away_team = request.POST['away']
        home_name = request.POST['homename']
        away_name = request.POST['awayname']
        if bet_type == 'O':
            form = overUnder(request.POST)
            if form.is_valid():
                over_under = form.cleaned_data['over_under']
                amount = form.cleaned_data['amount']
                try:
                    balance = neo4j.Get_Balance(user)
                    if amount>balance:
                        newForm = overUnder(initial=form.cleaned_data)
                        return render(request, "bets.html", {'form':newForm, 'msg':f'Not enough funds. {balance} available.', 'user':user, 'home':home_team, 'away':away_team, 'game':game, 'type':bet_type})
                except:
                    pass
                temp = RavenDB.overUnderBet(amount, user, over_under, game)
                middlelayer.Logging('CREATE', temp)
                return homeRender(request, user)
            return render(request, "home.html", {'error':form.errors})
        if bet_type == 'M':
            form = moneyLine([(home_team, home_name), (away_team, away_name)], request.POST)
            if form.is_valid():
                winner = form.cleaned_data['winner']
                amount = form.cleaned_data['amount']
                try:
                    balance = neo4j.Get_Balance(user)
                    if amount>balance:
                        newForm = moneyLine([(home_team, home_name), (away_team, away_name)], initial=form.cleaned_data)
                        return render(request, "bets.html", {'form':newForm, 'msg':f'Not enough funds. {balance} available.', 'user':user, 'home':home_team, 'away':away_team, 'game':game, 'type':bet_type})
                except:
                    pass
                temp = RavenDB.moneyLineBet(winner, amount, user, game)
                middlelayer.Logging('CREATE', temp)
                return homeRender(request, user)
            print(form.fields['winner'].choices)
            return render(request, "home.html", {'error':form.errors})


def stats(request):
    return render(request, 'stats.html', {})