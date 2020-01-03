# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def welcome(request):
    logging.info(request)
    return HttpResponse("Hello, World!")


def hello(request):
    today = datetime.datetime.now()
    return render(request, "hello.html", {"today": today})
