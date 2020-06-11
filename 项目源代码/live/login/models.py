from django.db import models

# Create your models here.
class User(models.Model):
    gender = (('male','男'),('female','女'))

    name = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=100,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name==other.name

    class Meta:
        ordering = ["-c_time"]
        # verbose_name = "用户"
        # verbose_name_plural = "用户"