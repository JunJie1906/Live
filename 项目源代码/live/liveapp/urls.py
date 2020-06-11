from django.urls import path, re_path
from . import views


app_name = 'liveapp'

urlpatterns = [
    path('launch/', views.launch),
    path('live/<pk>/', views.live, name='lives'),
    path('findlive/',views.FindLive),
    path('mylive/',views.MyLive),
    path('opencamera/',views.openCamera),
    path('closecamera/',views.closeCamera),
    path('closelive/',views.closelive),
    path('openShareScreen/',views.openShareScreen),
]
