#
# Import Python
from django.core.mail import message
from apps.codes.models import AuthenticationKey
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
#
# Import Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404

#
# Import Models
from ..userprofile.models import Userprofile, ResetPassword
from ..team.models import Team, Invitation
from ..project.models import Entry
from ..logs.models import Logs
from ..codes.models import AuthenticationKey
from ..event.models import Event

#
# Import utilities
from .utilities import get_time_for_user_and_day, get_time_for_user_and_month, get_time_for_user_and_project_and_month
from .decorators import user_passes_test

#
# Import Permissions
from apps.core import permissions as per
# Views


@login_required
@user_passes_test(per.user_required_group, level='User')
def dashboard(request):
    if request.user.is_authenticated:
        # search bar,
        if request.method == 'POST':
            if request.POST.get('date'):
                date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')

                if date.date() > datetime.now().date():
                    messages.info(request, "You can't look into the future! :D")
                    return redirect('dashboard')
                all_projects_time = []
                all_projects_title = []
                # Set variables

                team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
                members = team.members.all()

                # User date, pagination

                num_days = (datetime.now() - date).days
                date_user = datetime.now() - timedelta(days=num_days)
                date_entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=date_user,
                                                    is_tracked=True)
                no_tracked_entries = Entry.objects.filter(team=team, created_by=request.user, is_tracked=False)

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
                                                                                                          request.user,
                                                                                                          project,
                                                                                                          user_month)

                    all_projects_time.append(project.time_for_user_and_project_and_month)
                    all_projects_title.append(project.title)
                time_for_user_month = get_time_for_user_and_month(user=request.user, team=team, date=user_month)
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
                    'time_for_user_and_date': get_time_for_user_and_day(user=request.user, team=team, date=date_user),
                    'time_for_user_and_month': time_for_user_month['total'],
                    'time_for_user_and_month_approved': time_for_user_month['approved'],
                    'time_for_user_and_month_disapproved': time_for_user_month['disapproved'],
                    'time_for_user_and_month_waiting': time_for_user_month['waiting'],
                }
                return render(request, 'core/dashboard.html', context)

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

        # User date, pagination

        num_days = int(request.GET.get('num_days', 0))
        date_user = datetime.now() - timedelta(days=num_days)
        date_entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=date_user,
                                            is_tracked=True)
        no_tracked_entries = Entry.objects.filter(team=team, created_by=request.user, is_tracked=False)

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
            project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, request.user,
                                                                                                  project, user_month)

            all_projects_time.append(project.time_for_user_and_project_and_month)
            all_projects_title.append(project.title)
        time_for_user_month = get_time_for_user_and_month(user=request.user, team=team, date=user_month)

        # Events

        events = Event.objects.filter(user=request.user, date__month=user_month.month)

        context = {
            'event': events,
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
            'time_for_user_and_date': get_time_for_user_and_day(user=request.user, team=team, date=date_user),
            'time_for_user_and_month': time_for_user_month['total'],
            'time_for_user_and_month_approved': time_for_user_month['approved'],
            'time_for_user_and_month_disapproved': time_for_user_month['disapproved'],
            'time_for_user_and_month_waiting': time_for_user_month['waiting'],
        }
        return render(request, 'core/dashboard.html', context)


def reset_pass(request):
    code = request.GET.get('c')
    authenticate = get_object_or_404(AuthenticationKey, key=code)
    reset_pass = get_object_or_404(ResetPassword, auth_key=authenticate)
    if (authenticate.created_at + timedelta(minutes=15)) < datetime.now(pytz.utc):
        reset_pass.delete()
        logout(request)
        return redirect('login_')

    if request.method == 'POST':
        authenticate = get_object_or_404(AuthenticationKey, key=code)
        reset_pass = get_object_or_404(ResetPassword, auth_key=authenticate)
        user = reset_pass.created_by
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 == password2:
            print(password1)
            user.set_password(password1)
            user.save()
            team = get_object_or_404(Team, pk=user.userprofile.team_id)
            Logs.objects.create(team=team, note=f"Password was changed for account {user.username}", created_by=user)
            messages.info(request, 'Password was successfuly changed! You can login with your new password now.')
            reset_pass.delete()
            logout(request)

            return redirect('login_')
        else:
            return redirect('reset_pass')
    

    return render(request, 'core/reset_password.html', {'auth_key': authenticate.key})



def signup(request):
    code = request.GET.get('c')
    authentication = get_object_or_404(AuthenticationKey, key=code)
    invitation = get_object_or_404(Invitation, auth_key=authentication, is_active=True)
    is_ceo = invitation.is_ceo
    team = Team.objects.get(pk=invitation.team)
    if invitation:
        if invitation.is_active:
            email = invitation.email
            if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.email = user.username
                    user.save()
                    userprofile = Userprofile.objects.create(user=user, team_id=team.id, is_ceo=is_ceo)
                    team.members.add(user)
                    team.save()

                    invitation.delete()

                    login(request, user)

                    Logs.objects.create(team=team, note=f"Created new account {email}", created_by=user)

                    messages.info(request, 'Thank you for choosing our product :)')

                    return redirect('dashboard')

            else:
                form = UserCreationForm()

            return render(request, 'core/signup.html', {'form': form, 'email': email, 'code': code})
    else:
        return redirect('page_not_found')


def error_404(request, exception):
    data = {}
    return render(request, 'core/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'core/500.html', data)
