#
# Import Python
import datetime

#
# Import Models
from ..project.models import Entry


# functions


def get_time_for_user_and_day(user, team, date):
    entries = Entry.objects.filter(created_by=user, team=team, created_at__date=date, is_tracked=True)
    return sum(entry.minutes for entry in entries)


def get_time_for_user_and_day_and_project(user, team, date, project):
    total = Entry.objects.filter(created_by=user, team=team, created_at__date=date, is_tracked=True, project=project)
    approved = Entry.objects.filter(created_by=user, team=team, created_at__date=date, is_tracked=True, project=project,
                                    checked=True, approved=True)
    disapproved = Entry.objects.filter(created_by=user, team=team, created_at__date=date, is_tracked=True, project=project,
                                       checked=True, approved=False)
    waiting = Entry.objects.filter(created_by=user, team=team, created_at__date=date, is_tracked=True, project=project,
                                   checked=False, approved=False)

    return {'total': sum(entry.minutes for entry in total),
            'approved': sum(entry.minutes for entry in approved),
            'disapproved': sum(entry.minutes for entry in disapproved),
            'waiting': sum(entry.minutes for entry in waiting)}


def get_time_for_user_and_month(user, team, date):
    total = Entry.objects.filter(created_by=user, team=team, created_at__year=date.year, created_at__month=date.month,
                                 is_tracked=True)

    disapproved = Entry.objects.filter(created_by=user, team=team, created_at__year=date.year, created_at__month=date.month,
                                       is_tracked=True, checked=True, approved=False)

    approved = Entry.objects.filter(created_by=user, team=team, created_at__year=date.year, created_at__month=date.month,
                                    is_tracked=True, checked=True, approved=True)

    waiting = Entry.objects.filter(created_by=user, team=team, created_at__year=date.year, created_at__month=date.month,
                                   is_tracked=True, checked=False, approved=False)

    return {'total': sum(entry.minutes for entry in total),
            'approved': sum(entry.minutes for entry in approved),
            'disapproved': sum(entry.minutes for entry in disapproved),
            'waiting': sum(entry.minutes for entry in waiting)}


def get_time_for_user_and_project_and_month(team, user, project, month):
    entries = Entry.objects.filter(project=project, team=team, created_by=user, created_at__year=month.year,
                                   created_at__month=month.month, is_tracked=True)
    return sum(entry.minutes for entry in entries)

