#
# Import Python
from datetime import timezone, datetime
#
# Import Django
from django.db import models

#
# Import Models
from ..team.models import Team
from django.contrib.auth.models import User

#
# Models


class Project(models.Model):
    title = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name='project', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name='project', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def num_of_tasks(self):
        return self.task.filter(status=Task.TODO).count()

    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())


class Task(models.Model):

    TODO = 'todo'
    DONE = 'done'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        (TODO, 'Todo'),
        (DONE, 'Done'),
        (ARCHIVED, 'Archived'),
    )

    team = models.ForeignKey(Team, related_name='task', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='task', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, related_name='task', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=TODO)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())


class Entry(models.Model):
    team = models.ForeignKey(Team, related_name='entries', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    set_minutes = models.IntegerField(default=5)
    minutes = models.IntegerField(default=0)
    note = models.CharField(max_length=100, default='------')
    is_tracked = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.task:
            return '%s - %s' % (self.task, self.created_at)
        else:
            return '%s' % self.created_at