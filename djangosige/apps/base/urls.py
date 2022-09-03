# -*- coding: utf-8 -*-

from django.urls import re_path as url
from . import views

from djangosige.configs import DEBUG

app_name = 'djangosige.apps.base'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]

if DEBUG:
    urlpatterns += [
        url(r'^404/$', views.handler404),
        url(r'^500/$', views.handler500),
    ]
