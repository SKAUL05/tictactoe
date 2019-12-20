# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def hello(request):
    today = datetime.datetime.now().date()
    return render(request, "hello.html", {"today": today})