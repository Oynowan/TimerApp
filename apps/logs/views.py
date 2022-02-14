# 
# Import Python
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import csv

#
# Import Django
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

#
# Import Utilities
from ..core.utilities import get_time_for_user_and_month, get_time_for_user_and_day, get_time_for_user_and_day_and_project, get_time_for_user_and_project_and_month
from .utilities import number_of_days
from apps.core import permissions as per

#
# Import Models
from ..userprofile.models import User
from ..team.models import Team
from ..project.models import Entry
from .models import Logs

#
# import decorators
from ..core.decorators import user_passes_test

@login_required
@user_passes_test(per.user_required_group, level='HR')
def csv_file(request, user_id, user_num_months=0):
    user = get_object_or_404(User, pk=user_id)
    team = get_object_or_404(Team, pk=user.userprofile.team_id)
    user_month = datetime.now() - relativedelta(months=user_num_months)
    waiting_entries = Entry.objects.filter(team=team, checked=False, approved=False, is_tracked=True, created_at__month=user_month.month, created_by=user)
    entries = Entry.objects.filter(team=team, checked=True, is_tracked=True, created_at__month=user_month.month, created_by=user)
    
    # Check if any waiting entries 
    if waiting_entries:
        messages.info(request,'There is still waiting entry to approve/disapprove for that user. Please resolve these issue and try again.')
        return redirect('users_profile', user_id)
    days = number_of_days(user_month.year, user_month.month)
    file = [['', '', 'Date:'], ['', '',], ['', 'Project',]]
    space = ['',]
    projects_ = team.project.all()
    projects = []

    for project in projects_:
        minutes = get_time_for_user_and_project_and_month(team, user, project, user_month)
        if  minutes > 0:
            projects.append(project)

    response = HttpResponse()
    response['Content-Disposition'] = f'attachment; filename={user.first_name}_{user.last_name}_{user_month.month}_{user_month.year}.csv'

    # User month, pagination
    writer = csv.writer(response)
    for j in range(1, 4):
        writer.writerow([''])
    writer.writerow(['', '', f'Team: {team.title}',])
    writer.writerow(['', '', f'Employee: {user.first_name} {user.last_name}', ])
    writer.writerow([''])

    # Dates of the month till now
    for i in range(1, days+1):
        if datetime.now().day < i and datetime.now().month == user_month.month:
            break
        user_month = user_month.replace(day=i)
        file[1].append(user_month.date())
        space.append('')

    # Time for project
    x = 3
    today_day = datetime.now().day
    today_month = datetime.now().month
    for project in projects:
        file.append(['', f'{project.title}:', ])
        for i in range(1, days+1):
            if today_day < i and today_month == user_month.month:
                break
            user_month = user_month.replace(day=i)

            minutes = get_time_for_user_and_day_and_project(user=user, team=team, date=user_month, project=project)
            if minutes['total'] != 0:
                if minutes['approved'] != 0:
                    hours, min = divmod(minutes['approved'], 60)
                    file[x].append(f'{hours}h {min}m (approved)')
                else:
                    hours, min = divmod(minutes['disapproved'], 60)
                    file[x].append(f'{hours}h {min}m (disapproved)')
            else:
                file[x].append('------')
        x += 1
    for row in file:
        writer.writerow(row)

    minutes = get_time_for_user_and_month(user_id, team.id, user_month)
    for key, value in minutes.items():
        if key == "waiting":
            pass
        hours, minutes = divmod(value, 60)
        writer.writerow([''])
        space.append(key.upper())
        writer.writerow(space)
        del space[-1]
        space.append(f'{hours}h {minutes}m')
        writer.writerow(space)

    """
    writer.writerow(['', 'First Name', 'Last Name', 'Date', 'Time'])
    writer.writerow(['', user.first_name, user.last_name, f'{user_month.month}.{user_month.year}', ''])
    for i in range(1, days+1):
        if datetime.now().day < i and datetime.now().month == user_month.month:
            break
        user_month = user_month.replace(day=i)
        time = get_time_for_user_and_day(user, team, user_month)
        hours, minutes = divmod(time, 60)
        writer.writerow(['','', '', user_month.date(), f'{hours}h {minutes}m'])
    time = get_time_for_user_and_month(user_id, team.id, user_month)
    hours, minutes = divmod(time, 60)
    writer.writerow(['','', '', '', '', 'Total'])
    writer.writerow(['','', '', '', '', f'{hours}h {minutes}m'])
    """
    Logs.objects.create(team=team, note=f"Downloaded Logs of {user} for month {user_month.month}", created_by=request.user)
    return response


@login_required
@user_passes_test(per.user_required_group, level='HR')
def list_of_waiting_entries(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    entries = Entry.objects.filter(team=team, checked=False, approved=False, is_tracked=True)
    return render(request, 'logs/list_of_waiting_entries.html', {'entries':entries, 'team': team})

@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def all_logs(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    logs = Logs.objects.filter(team=team)

    paginator = Paginator(logs, 100)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'logs/full_logs.html', {'page_obj': page_obj})

@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def approve_all_entries(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    entries = Entry.objects.filter(team=team, checked=False, approved=False, is_tracked=True)

    for entry in entries:
        entry.checked = True
        entry.approved = True

        entry.save()

        Logs.objects.create(team=team, note=f"Entry {entry.created_by} - {entry.created_at} - {entry.minutes} "
                                            f"was approved", created_by=request.user)
    
    messages.info(request, "All entries were successfully approved!")

    entries = Entry.objects.filter(team=team, checked=False, approved=False, is_tracked=True)

    return render(request, 'logs/list_of_waiting_entries.html', {'entries': entries, 'team': team})