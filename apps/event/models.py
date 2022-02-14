from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):

    title = models.CharField(max_length=255)
    date = models.DateField()
    start_date = models.DateField()
    last_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    minutes = models.IntegerField(null=True, blank=True)
    bussy = models.BooleanField(default=False)
    longer_time = models.BooleanField(default=False)
    parent = models.BooleanField(default=True)
    parent_id = models.IntegerField(blank=True, null=True)
    child = models.BooleanField(default=False)
    last_event_day = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        if self.title:
            return self.title
        return self.date