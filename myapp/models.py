# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import logging

GAME_STATUS_CHOICES = (
    ("F", "First Player To Move"),
    ("S", "Second Player To Move"),
    ("W", "First Player Wins"),
    ("L", "Second Player Wins"),
    ("D", "Draw"),
)
BOARD_SIZE = 3


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

    def board(self):
        """Return a 2-dimensional list of Move objects
          so you can ask for the state of a square at position [x][y]."""
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        return (user == self.firstPlayer and self.status == 'F') or \
               (user == self.secondPlayer and self.status == 'S')

    def get_absolute_url(self):
        return reverse('gameplay_detail',args=[self.id])

    def new_move(self):
        """Returns a new move object with player, game, and count preset"""
        if self.status not in 'FS':
            raise ValueError("Cannot make move on finished game")
        return Move(
            game=self,
            firstPlayerMove=self.status == 'F'
        )

    def update_after_move(self, move):
        """Update the status of the game, given the last move"""
        print("Here")
        self.status = self._get_game_status_after_move(move)
        print(self.status)

    def _get_game_status_after_move(self, move):
        x, y = move.x, move.y
        board = self.board()
        if ((board[y][0] == board[y][1] == board[y][2]) or (board[0][x] == board[1][x] == board[2][x]) or (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0])) and ((board[y][0] or board[y][1]  or board[y][2]) and (board[0][x] or board[1][x] or board[2][x]) and (board[0][0] or board[1][1] or board[2][2]) and (board[0][2] or board[1][1] or board[2][0])):
            return "W" if move.firstPlayerMove else "L"
        if self.move_set.count() >= BOARD_SIZE ** 2:
            return 'D'
        return 'S' if self.status == 'F' else 'F'

    def __str__(self):
        return "{0} vs {1}".format(self.firstPlayer, self.secondPlayer)


class Move(models.Model):
    x = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    y = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    comment = models.CharField(max_length=300, blank=True)
    game = models.ForeignKey(Game, editable=False, on_delete=models.CASCADE)
    firstPlayerMove = models.BooleanField(editable=False)

    def __eq__(self, other):
        if other is None:
            return False
        return other.firstPlayerMove == self.firstPlayerMove

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        print(self.game)
        self.game.save()