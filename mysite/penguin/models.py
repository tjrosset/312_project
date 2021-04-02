from django.db import models

# Create your models here.
# python manage.py migrate
class Post(models.Model):
    content_text = models.CharField(max_length= 200)