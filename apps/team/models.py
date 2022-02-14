#
# Import Django
from django.db import models
from django.contrib.auth.models import User

#
# Import Models
from ..codes.models import AuthenticationKey

# Models


class Invitation(models.Model):
    auth_key = models.ForeignKey(AuthenticationKey, on_delete=models.CASCADE)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ceo = models.BooleanField(default=False)
    team = models.IntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Team(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='team')
    created_by = models.ForeignKey(User, related_name='created_team', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
