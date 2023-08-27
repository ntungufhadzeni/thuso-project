from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list, name='football_betting'),
]
