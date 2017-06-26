# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'base'
urlpatterns = [	
	url(r'^$', views.IndexView.as_view(), name='index'),
]