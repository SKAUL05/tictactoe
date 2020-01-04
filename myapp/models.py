# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

GAME_STATUS_CHOICES = (
    ("F", "First Player To Move"),
    ("S", "Second Player To Move"),
    ("W", "First Player Wins"),
    ("L", "Second Player Wins"),
    ("D", "Draw"),
)


class GameQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(Q(firstPlayer=user) | Q(secondPlayer=user))

    def active(self):
        return self.filter(Q(status="F") | Q(status="S"))

    def draw(self):
        return self.filter(status = 'D')


class Game(models.Model):
    firstPlayer = models.ForeignKey(
        User, related_name="game_first_player", on_delete=models.CASCADE
    )
    secondPlayer = models.ForeignKey(
        User, related_name="game_second_player", on_delete=models.CASCADE
    )
    startTime = models.DateTimeField(auto_now_add=True)
    lastActive = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default="F", choices=GAME_STATUS_CHOICES)

    manager = GameQuerySet.as_manager()

    def __str__(self):
        return "{0} vs {1}".format(self.firstPlayer, self.secondPlayer)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    firstPlayerMove = models.BooleanField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
