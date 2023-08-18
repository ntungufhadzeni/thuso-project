
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('cover-letter/', views.whatsapp_webhook, name='whatsapp-webhook')
]


