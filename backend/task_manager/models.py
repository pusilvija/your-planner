from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='to do')
    description = models.TextField()
    category = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
