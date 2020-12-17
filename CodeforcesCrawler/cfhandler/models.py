from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class languages(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name

class verdicts(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name

class levels(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name
