from django.conf.urls import url

from djangosige.configs import DEBUG

from . import views

app_name = "base"
urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
]

if DEBUG:
    urlpatterns += [
        url(r"^404/$", views.handler404),
        url(r"^500/$", views.handler500),
    ]
