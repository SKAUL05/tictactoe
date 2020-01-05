# Created by sarathkaul on 04/01/20

from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, new_invitation, accept_invitation

urlpatterns = [
    url(r"home$", home, name="player_home"),
    url(r'login', LoginView.as_view(template_name = "player/login_form.html"), name ="player_login"),
    url(r'new_invitation$',new_invitation, name = "invitation_form"),
    url(r'accept_invitation/(?P<id>\d+)/$',accept_invitation, name= "player_accept_invitation"),
    url(r'logout$', LogoutView.as_view(), name ="player_logout")
]
