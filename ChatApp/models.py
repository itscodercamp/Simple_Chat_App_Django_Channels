from django.db import models

# Create your models here.
class ChatsRoom(models.Model):
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Groups(models.Model):
    group_name = models.CharField(max_length=200)

    def __str__(self):
        return self.group_name