# Created by sarathkaul on 04/01/20
from django.forms import ModelForm
from .models import Invitation

class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ('fromUser', 'timestamp')

