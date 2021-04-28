from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    hash = models.CharField(max_length=64)
    created_date = models.DateTimeField

    def __str__(self):
        return self.user
