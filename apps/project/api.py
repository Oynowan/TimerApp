#
# Import Python
import json
from datetime import datetime, timezone
#
# Import Django
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#
# Import Models
from .models import Project, Entry, Task
from ..team.models import Team
from ..logs.models import Logs
from ..userprofile.models import Userprofile

#
# Import decorators
from apps.core.decorators import user_passes_test

from apps.core import permissions as per
# API View

@login_required
def api_start_timer(request):
    team = Team.objects.get(pk=request.user.userprofile.team_id)
    set_minutes = json.loads(request.body)["set_times"]
    entry = Entry.objects.create(team=team, minutes=0, created_by=request.user, is_tracked=False, set_minutes=int(set_minutes))

    Logs.objects.create(team=team, note="Started timer", created_by=request.user)

    return JsonResponse({'success': True, 'set_minutes': set_minutes})

@login_required
def api_stop_timer(request):
    team = Team.objects.get(pk=request.user.userprofile.team_id)
    entry = Entry.objects.get(team=team, created_by=request.user, minutes=0, is_tracked=False)

    tracked_minutes = int((datetime.now(timezone.utc) - entry.created_at).total_seconds() / 60)

    if tracked_minutes < 1:
        tracked_minutes = 1

    if tracked_minutes >= entry.set_minutes:
        tracked_minutes = entry.set_minutes

    entry.minutes = tracked_minutes
    entry.is_tracked = False
    entry.save()

    Logs.objects.create(team=team, note=f"Stopped timer and tracked {entry.minutes} minutes", created_by=request.user)

    return JsonResponse({'success': True, 'entryID': entry.id})

@login_required
def api_discard_timer(request):
    team = Team.objects.get(pk=request.user.userprofile.team_id)
    entries = Entry.objects.filter(team=team, created_by=request.user, is_tracked=False).order_by('-created_at')

    if entries:
        entry = entries.first()
        Logs.objects.create(team=team, note=f"Discarded entry {entry.created_at.date()} - {entry.minutes}min",
                            created_by=request.user)

        entry.delete()

    return JsonResponse({'success': True})

@login_required
def api_get_tasks(request):
    project_id = request.GET.get('project_id', '')

    if project_id:
        tasks = []
        team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
        project = get_object_or_404(Project, pk=project_id, team=team)

        for task in project.task.filter(status='todo'):
            obj = {
                'id': task.id,
                'title': task.title
            }
            tasks.append(obj)

        return JsonResponse({'success': True, 'tasks': tasks})

    return JsonResponse({'success': False})

@login_required
@user_passes_test(per.user_required_group, level='HR')
def api_get_entries_to_check(request):
    if request.user.userprofile.is_ceo or request.user.userprofile.is_hr:
        entries = Entry.objects.filter(checked=False, approved=False, is_tracked=True)

        return JsonResponse({'success': True, 'entries': len(entries)})
    else:
        return JsonResponse({'success': False})

@login_required
@user_passes_test(per.user_required_group, level='HR')
def api_active_project(request):
    project_id = request.GET.get('project_id', '')

    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        team = get_object_or_404(Team, pk=request.user.userprofile.team_id)

        if project.active:
            Logs.objects.create(team=team, note=f"Project {project.title} was deactivated",
                            created_by=request.user)
        else:
            Logs.objects.create(team=team, note=f"Project {project.title} was activated",
                            created_by=request.user)

        project.active = not project.active
        project.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def api_set_hr(request):
    user_id = request.GET.get('user_id', '')

    if user_id:
        user = get_object_or_404(User, pk=user_id)
        userprofile = get_object_or_404(Userprofile, user=user)
        team = get_object_or_404(Team, pk=userprofile.team_id)

        if userprofile.is_hr:
            Logs.objects.create(team=team, note=f"HR for user {user.username} was deactivated",
                            created_by=request.user)
        else:
            Logs.objects.create(team=team, note=f"HR for user {user.username} was activated",
                            created_by=request.user)

        userprofile.is_hr = not userprofile.is_hr
        userprofile.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})