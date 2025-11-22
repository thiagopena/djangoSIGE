# -*- coding: utf-8 -*-

from django.urls import re_path

from djangosige.configs import DEBUG

from . import views

app_name = "base"
urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="index"),
]

if DEBUG:
    urlpatterns += [
        re_path(r"^404/$", views.handler404),
        re_path(r"^500/$", views.handler500),
    ]
