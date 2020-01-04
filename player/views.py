from django.shortcuts import render
from myapp.models import Game


def home(request):
    first_player = Game.objects.filter(
        firstPlayer = request.user,
        status = "F"
    )
    second_player = Game.objects.filter(
        secondPlayer = request.user,
        status = "S"
    )
    all_games = list(first_player) + list(second_player)


    return render(request, "player/home.html", {"games": all_games})
