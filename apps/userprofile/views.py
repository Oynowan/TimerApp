#
# Import Python
from apps.codes.models import AuthenticationKey
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import string

#
# Import django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Import Models
from .models import Userprofile, ResetPassword
from ..team.models import Team
from ..logs.models import Logs
from ..project.models import Entry, Task, Project
from ..core.utilities import get_time_for_user_and_day, get_time_for_user_and_month, get_time_for_user_and_project_and_month

# Import decorator
from ..core.decorators import user_passes_test

# Utilities 
from ..emails.utilities import reset_password_email
from apps.core import permissions as per


# Views


@login_required
@user_passes_test(per.user_required_group, level='User')
def myaccount(request):
    teams = Team.objects.filter(members__in=[request.user])
    return render(request, 'userprofile/myaccount.html', {'teams': teams})


@login_required
@user_passes_test(per.user_required_group, level='User')
def edit_profile(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    if request.method == 'POST':
        if request.user.first_name != request.POST.get('first_name', ''):
            Logs.objects.create(team=team,
                                note=f"First name has been changed from '{request.user.first_name}' "
                                     f"to '{request.POST.get('first_name', '')}'",
                                created_by=request.user)

        if request.user.last_name != request.POST.get('last_name', ''):
            Logs.objects.create(team=team,
                                note=f"Last name has been changed from '{request.user.last_name}' "
                                     f"to '{request.POST.get('last_name', '')}'",
                                created_by=request.user)
        """
        if request.user.email != request.POST.get('email', ''):
            Logs.objects.create(team=team,
                                note=f"Email has been changed from '{request.user.email}' "
                                     f"to '{request.POST.get('email', '')}'",
                                created_by=request.user)
        """
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        #request.user.email = request.POST.get('email', '')
        request.user.save()

        if request.FILES:
            avatar = request.FILES['avatar']
            userprofile = request.user.userprofile
            userprofile.avatar = avatar
            userprofile.save()



        messages.info(request, 'You profile was saved.')

        return redirect('myaccount')

    return render(request, 'userprofile/edit_profile.html')

@login_required
@user_passes_test(per.user_required_group, level='User')
def reset_password(request):
    while True:
        code = ''.join(random.choice(string.ascii_letters + '0123456789') for i in range(30))
        if not AuthenticationKey.objects.filter(key=code):
            team = get_object_or_404(Team, id=request.user.userprofile.team_id)
            auth = AuthenticationKey.objects.create(key=code)
            ResetPassword.objects.create(created_by=request.user, auth_key=auth)
            reset_password_email(request.user.username, f'?c={code}')

            Logs.objects.create(team=team, note=f"Requested password reset for account {request.user.username}", created_by=request.user)

            messages.info(request, 'Link to reset your password was sent to your email. It is active for 15 minutes.')

            teams = Team.objects.filter(members__in=[request.user])
            return redirect('myaccount')


@login_required
@user_passes_test(per.user_required_group, level='HR')
def users_profile(request, user_id):
    if request.method == 'POST':
        if request.POST.get('date'):
            date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')

            if date.date() > datetime.now().date():
                messages.info(request, "You can't look into the future! :D")
                return redirect('users_profile', user_id)
            all_projects_time = []
            all_projects_title = []
            # Set variables
            user = get_object_or_404(User, pk=user_id)
            team = get_object_or_404(Team, pk=user.userprofile.team_id)
            members = team.members.all()
            # User date, pagination

            num_days = (datetime.now() - date).days
            date_user = datetime.now() - timedelta(days=num_days)
            date_entries = Entry.objects.filter(team=team, created_by=user, created_at__date=date_user,
                                                    is_tracked=True)
            no_tracked_entries = Entry.objects.filter(team=team, created_by=user, is_tracked=False)

            # User month, pagination

            user_num_months = int(request.GET.get('user_num_months', 0))
            user_month = datetime.now() - relativedelta(months=user_num_months)

            # Projects
                
            all_projects_ = team.project.all()
            all_projects = []

            for project in all_projects_:
                time = get_time_for_user_and_project_and_month(team, request.user, project, user_month)
                if time > 0:
                    all_projects.append(project)

            for project in all_projects:
                project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team,
                                                                                                        user,
                                                                                                        project,
                                                                                                        user_month)

                all_projects_time.append(project.time_for_user_and_project_and_month)
                all_projects_title.append(project.title)
            time_for_user_month = get_time_for_user_and_month(user=user, team=team, date=user_month)
            context = {
                'num_days': num_days,
                'date_user': date_user,
                'date_entries': date_entries,
                'no_tracked_entries': no_tracked_entries,
                'all_projects': all_projects,
                'all_projects_time': all_projects_time,
                'all_projects_title': all_projects_title,
                'user_num_months': user_num_months,
                'user_month': user_month,
                'members': members,
                'time_for_user_and_date': get_time_for_user_and_day(user=user, team=team, date=date_user),
                'time_for_user_and_month': time_for_user_month['total'],
                'time_for_user_and_month_approved': time_for_user_month['approved'],
                'time_for_user_and_month_disapproved': time_for_user_month['disapproved'],
                'time_for_user_and_month_waiting': time_for_user_month['waiting'],
            }
            return render(request, 'userprofile/users_profile.html', context)
        search = request.POST.get('search').lower()
        team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
        profiles = []
        for member in team.members.all():
            if search in member.username.lower() or search in member.first_name.lower() or search in member.last_name.lower():
                profiles.append(member)

        return render(request, 'userprofile/search_profile.html', {'search': search, 'profiles': profiles})

    all_projects_time = []
    all_projects_title = []
    # Set variables

    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    all_projects = team.project.all()
    members = team.members.all()
    user = get_object_or_404(User, pk=user_id)

    # User date, pagination

    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_entries = Entry.objects.filter(team=team, created_by=user, created_at__date=date_user,
                                            is_tracked=True)
    no_tracked_entries = Entry.objects.filter(team=team, created_by=user, is_tracked=False)

    # User month, pagination

    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)

    # Projects
                
    all_projects_ = team.project.all()
    all_projects = []
    for project in all_projects_:
        time = get_time_for_user_and_project_and_month(team, user, project, user_month)
        if time > 0:
            all_projects.append(project)

    for project in all_projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, user,
                                                                                                  project, user_month)
        all_projects_time.append(project.time_for_user_and_project_and_month)
        all_projects_title.append(project.title)

    time_for_user_month = get_time_for_user_and_month(user=user, team=team, date=user_month)
    context = {
        'num_days': num_days,
        'user': user,
        'date_user': date_user,
        'date_entries': date_entries,
        'no_tracked_entries': no_tracked_entries,
        'all_projects': all_projects,
        'all_projects_time': all_projects_time,
        'all_projects_title': all_projects_title,
        'user_num_months': user_num_months,
        'user_month': user_month,
        'members': members,
        'time_for_user_and_date': get_time_for_user_and_day(user=user, team=team, date=date_user),
        'time_for_user_and_month': time_for_user_month['total'],
        'time_for_user_and_month_approved': time_for_user_month['approved'],
        'time_for_user_and_month_disapproved': time_for_user_month['disapproved'],
        'time_for_user_and_month_waiting': time_for_user_month['waiting'],
    }
    return render(request, 'userprofile/users_profile.html', context)
