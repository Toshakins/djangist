from django.db import models

# Create your models here.

class Numbers(models.Model):
    number = models.IntegerField()