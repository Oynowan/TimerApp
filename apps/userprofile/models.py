#
# Import Django
from apps.codes.models import AuthenticationKey
from django.db import models
from django.contrib.auth.models import User


# Models
from ..team.models import Team


class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    team_id = models.IntegerField()
    is_ceo = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=f'uploads/avatars/', blank=True, null=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/images/avatar.png'

class ResetPassword(models.Model):
    auth_key = models.ForeignKey(AuthenticationKey, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username