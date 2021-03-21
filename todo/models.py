from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class GroupModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)
    group_description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.group_name


class TodosModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False, null=False)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
