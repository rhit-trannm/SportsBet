"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('acct', views.acct, name='acct'),
    path('bets', views.bets, name='bets'),
    path('stats', views.stats, name='stats'),
    path('friends', views.friends, name='friends'),
    path('players', views.players, name='players'),
    path('playerstats', views.playerstats, name='playerstats'),
    path('games', views.games, name='games'),
    path('teamstats', views.teamstats, name='teamstats'),
    path('bet', views.placeBet, name='bet'),
    path('wallet', views.wallet, name='wallet'),
]
