from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")  
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default='to do', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
