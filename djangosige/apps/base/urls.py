from django.urls import re_path
from . import views

from djangosige.configs import DEBUG

app_name = 'base'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]

if DEBUG:
    urlpatterns += [
        re_path(r'^404/$', views.handler404),
        re_path(r'^500/$', views.handler500),
    ]
