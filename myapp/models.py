# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

GAME_STATUS_CHOICES = (
    ("F", "First Player To Move"),
    ("S", "Second Player To Move"),
    ("W", "First Player Wins"),
    ("L", "Second Player Wins"),
    ("D", "Draw"),
)


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

    def __str__(self):
        return "{0} vs {1}".format(self.firstPlayer, self.secondPlayer)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    firstPlayerMove = models.BooleanField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
