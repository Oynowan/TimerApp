from django.db import models

# Create your models here.

class AuthenticationKey(models.Model):
    key = models.CharField(max_length=30, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key