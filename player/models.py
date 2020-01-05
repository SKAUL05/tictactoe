from django.db import models
from django.contrib.auth.models import User


class Invitation(models.Model):
    fromUser = models.ForeignKey(User, related_name="invitation_sent", on_delete=models.CASCADE)
    toUser = models.ForeignKey(User, related_name="invitation_received", on_delete=models.CASCADE, verbose_name="User to invite", help_text="Please select the user you want to play game with.")
    message = models.CharField(max_length=300, blank=True, verbose_name="Optional Message", help_text="Friendly Message")
    timestamp = models.DateTimeField(auto_now_add=True)

