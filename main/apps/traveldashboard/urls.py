from django.conf.urls import url, include
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^travels/new$', views.new),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/join/(?P<id>\d+)$', views.join)
]
