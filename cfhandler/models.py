from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Languages(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name

class Verdicts(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name

class Levels(models.Model):
    name = models.CharField(max_length = 200)
    val = models.IntegerField()

    def __str__(self):
        return self.name

class Chatroom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.user1) + str(self.user2)

    class Meta:
        unique_together = (("user1", "user2"),)

class Chatmessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    chatroom = models.ForeignKey(Chatroom, on_delete = models.CASCADE)

    def __str__(self):
        return self.message
