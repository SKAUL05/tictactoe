# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.


def welcome(request):
    logging.info(request)
    user_objs = User.objects.all()
    print ("Here",user_objs)
    return HttpResponse("Hello, World!")


def hello(request):
    today = datetime.datetime.now()
    return render(request, "hello.html", {"today": today})
