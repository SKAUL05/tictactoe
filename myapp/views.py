# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt


from .models import Game
from .forms import MoveForm


def welcome(request):
    logging.info(request)
    user_objs = User.objects.all()
    return HttpResponse("Hello, World!")


@login_required()
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    context = {"game": game}
    if game.is_users_move(request.user):
        context["form"] = MoveForm()
    return render(request, "gameplay/game_detail.html", context)


# @login_required()
@csrf_exempt
def make_move(request, id):
    import json

    data = json.loads(request.body)
    game = get_object_or_404(Game, pk=data["id"])
    if not game.is_users_move(request.user):
        raise PermissionDenied
    move = game.new_move()
    from django.http import QueryDict

    del data["id"]
    data["x"] = str(data["x"])
    data["y"] = str(data["y"])
    ordinary_dict = data
    query_dict = QueryDict("", mutable=True)
    query_dict.update(ordinary_dict)
    # < QueryDict: {'x': ['0'], 'y': ['2'], 'comment': [''],
    #               'csrfmiddlewaretoken': ['VGI47QxAjFvZVjV4LB9Or2ElwgJYfZmCRFftw8I7sHr2GpIrEbDqeIjicorQe0MM']} >

    form = MoveForm(instance=move, data=query_dict)
    if form.is_valid():
        move.save()
        return redirect("gameplay_detail", id)
    else:
        return render(
            request, "gameplay/game_detail.html", {"game": game, "form": form}
        )


class AllGamesList(ListView):
    model = Game
    template_name = "gameplay/game_list.html"
