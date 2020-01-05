# Created by sarathkaul on 04/01/20
from django.shortcuts import render, redirect

def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, "djangoLearn/welcome.html")