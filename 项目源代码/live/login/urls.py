from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('', views.index),

    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
]
