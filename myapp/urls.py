# Created by sarathkaul on 04/01/20

from django.conf.urls import url
from .views import hello

urlpatterns = [url(r"hello$", hello)]
