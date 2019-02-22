from django.conf.urls import url
from django.contrib import auth

from .views.reservations import ReservationFeed

from . import views

urlpatterns = [
    url(r'^$', views.space_reservations, name='r25'),
    url(r'^(?P<space_name>[^/]+)/?$',
        views.space_reservations, name='r25_space'),
    url(r'^(?P<space_name>[^/]+)/(?P<res_date>.+)/?$',
        views.space_reservations, name='r25_space_reservations'),

    url(r'^reservations.ics$', ReservationFeed()),
    url(r'^(?P<building>[a-zA-Z0-9]+)[ +_-](?P<room>[a-zA-Z0-9]+).ics$',
        ReservationFeed()),

    url(r'^logout/?$', auth.logout),
]
