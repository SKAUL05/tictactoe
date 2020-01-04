# Created by sarathkaul on 04/01/20
from django.shortcuts import render

def welcome(request):
    return render(request, "djangoLearn/welcome.html")