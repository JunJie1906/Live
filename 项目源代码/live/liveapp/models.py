from django.db import models
from django.urls import reverse

import login.models

class Live(models.Model):

    roomId = models.CharField(max_length=30,unique=True)
    creater = models.OneToOneField(login.models.User, on_delete=models.CASCADE, related_name='user',unique=True)
    roomName = models.CharField(max_length=128)

    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.roomName+"\n主持人："+self.creater.name

    def get_absolute_url(self):
        return reverse("liveapp:lives", kwargs={'pk': self.pk})


    class Meta:
        ordering = ["-c_time"]
        verbose_name = "直播"
        verbose_name_plural = "直播"



