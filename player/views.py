from django.shortcuts import render
from myapp.models import Game


def home(request):

    my_game = Game.manager.games_for_user(user=request.user)
    all_games = my_game.active()

    return render(request, "player/home.html", {"games": all_games})
