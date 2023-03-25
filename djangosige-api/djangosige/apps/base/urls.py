from django.conf import settings
from django.urls import re_path

from . import views

app_name = "base"
urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="index"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^404/$", views.handler404),
        re_path(r"^500/$", views.handler500),
    ]
