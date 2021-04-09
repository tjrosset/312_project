from django.db import models

# Create your models here.

class Player(models.Model):
    username = models.CharField(max_length=20)
    x_position = models.FloatField()
    y_position = models.FloatField()

    def __str__(self):
        return self.username
# python manage.py migrate
class Post(models.Model):
    content_text = models.CharField(max_length= 200)
