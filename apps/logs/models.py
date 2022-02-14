from django.db import models

from ..team.models import Team
from ..userprofile.models import User

# Create your models here.


class Logs(models.Model):
    note = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name="logs", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="logs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.note