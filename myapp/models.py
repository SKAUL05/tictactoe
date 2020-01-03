# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    firstPlayer = models.ForeignKey(User, related_name = "game_first_player")
    secondPlayer = models.ForeignKey(User, related_name = "game_second_player")
    startTime = models.DateTimeField(auto_now_add = True)
    lastActive = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 1)

class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length = 300, blank = True)
    firstPlayerMove = models.BooleanField()
    game = models.ForeignKey(Game)

