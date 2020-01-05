from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from myapp.models import Game
from .models import Invitation
from .forms import InvitationForm


@login_required
def home(request):
    my_game = Game.manager.games_for_user(user=request.user)
    all_games = my_game.active()
    invitations = request.user.invitation_received.all()
    finised_games = my_game.difference(all_games)
    return render(request, "player/home.html",
                  {"games": all_games,
                  "invitations": invitations,
                   "finished_games": finised_games}
                  )

@login_required()
def new_invitation(request):
    if request.method == "POST":
        invitation = Invitation(fromUser = request.user)
        form = InvitationForm(instance=invitation, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()

    return render(request, "player/new_invitation_form.html",{'form':form})

@login_required()
def accept_invitation(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.toUser:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.manager.create(
                firstPlayer=invitation.toUser,
                secondPlayer=invitation.fromUser,
            )
            invitation.delete()
            return redirect(game)
    else:
        return render(request,
                      "player/accept_invitation_form.html",
                      {'invitation': invitation}
                      )

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')


