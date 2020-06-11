# from django.conf.urls import re_path
from django.urls import path

from liveapp import consumers

websocket_urlpatterns = [
    path('ws/live/<pk>/', consumers.ChatConsumer),
]