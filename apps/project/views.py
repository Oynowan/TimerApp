# Import Python
from datetime import datetime
import pytz
#
# Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#
# Import Models
from .models import Project, Task, Entry
from ..team.models import Team
from ..logs.models import Logs

#
# Import Decorator
from ..core.decorators import user_passes_test
from apps.core import permissions as per
#
# Views


@login_required
@user_passes_test(per.user_required_group, level='User')
def projects(request):
    team = Team.objects.get(pk=request.user.userprofile.team_id)
    projects = Project.objects.filter(team=team, active=True)
    projects_disactivated = Project.objects.filter(team=team, active=False)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project = Project.objects.create(title=title, created_by=request.user, team=team, description=description)

        Logs.objects.create(team=team, note=f"Created new project {title}", created_by=request.user)
        messages.info(request, 'Project was created')

        return redirect('project:projects')
    return render(request, 'project/projects.html', {'projects': projects, 'projects_disactivated': projects_disactivated, 'team': team})


@login_required
@user_passes_test(per.user_required_group, level='CFO')
def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    team = get_object_or_404(Team, pk=project.team.id)
    tasks = Task.objects.filter(project=project, team=team)

    if request.method == 'POST':
        title = request.POST.get('title')
        task_todo = Task.objects.create(team=team, project=project, title=title, created_by=request.user)

        Logs.objects.create(team=team, note=f"Created new task {title}. Project {project.title}", created_by=request.user)
        messages.info(request, 'Task was created')

        return redirect('project:project_details', project_id)
    return render(request, 'project/project_details.html', {'project': project, 'tasks': tasks })


@login_required
@user_passes_test(per.user_required_group, level='HR')
def task_detail(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)
    entries = Entry.objects.filter(task=task)

    return render(request, 'project/task_detail.html', {'entries': entries, 'task': task, 'project': project})


@login_required
@user_passes_test(per.user_required_group, level='User')
def track_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    projects = team.project.all()

    if request.method == "POST":

        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')
        task = request.POST.get('task')
        description = request.POST.get('description')

        if datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date() > datetime.now().date():
            messages.info(request, "Can you see into the future how long you are going to work? ;)")
            return redirect('track_entry', entry_id)

        if project and task:
            entry.minutes = (hours * 60) + minutes
            entry.created_at = '%s %s' % (request.POST.get('date'), entry.created_at.time())
            entry.note = description
            entry.project = get_object_or_404(Project, pk=project)
            entry.task = get_object_or_404(Task, pk=task)
            entry.is_tracked = True
            entry.save()

            Logs.objects.create(team=team, note=f"Tracked entry {entry.created_at} - {entry.minutes}min - "
                                                f"{entry.project.title} {entry.task.title}", created_by=request.user)

            messages.info(request, 'The time was tracked')

            return redirect('dashboard')

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'hours': hours,
        'minutes': minutes,
        'entry': entry,
        'team': team,
        'projects': projects,
    }

    return render(request, 'project/track_entry.html', context)


@login_required
@user_passes_test(per.user_required_group, level='User')
def add_entry(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    projects = team.project.filter(active=True)

    if request.method == "POST":
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = get_object_or_404(Project, pk=request.POST.get('project'), active=True)
        task = get_object_or_404(Task, pk=request.POST.get('task'))
        description = request.POST.get('description')

        if datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date() > datetime.now().date():
            messages.info(request, "Can you see into the future how long you are going to work? ;)")
            return redirect('project:add_entry')

        time = '%s %s' % (request.POST.get('date'), datetime.now().time())
        if type(time) is str:
            utc_datetime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            local_time = pytz.timezone('Poland')
            local_datetime = local_time.localize(utc_datetime, is_dst=None)
            utc_datetime = local_datetime.astimezone(pytz.utc)
        if project and task:
            entry = Entry.objects.create(minutes=(hours * 60) + minutes, created_at=utc_datetime,
                                         note=description, project=project, task=task, created_by=request.user,
                                         is_tracked=True, team=team
                                         )
            Logs.objects.create(team=team, note=f"Created new entry {entry.created_at} - {entry.minutes}min - "
                                                f"{project.title} - {task.title}", created_by=request.user)

            messages.info(request, 'The entry was created')

            return redirect('dashboard')

    context = {
        'team': team,
        'projects': projects,
        'time': datetime.now(),
    }

    return render(request, 'project/add_entry.html', context)


@login_required
@user_passes_test(per.user_required_group, level='User')
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    if entry.created_by == request.user:
        if entry.is_tracked:
            Logs.objects.create(team=entry.team, note=f"Deleted entry {entry.created_at.date()} - "
                                                  f"{entry.minutes}min - {entry.project.title} {entry.task.title}",
                            created_by=request.user)
        else:
            Logs.objects.create(team=entry.team, note=f'Deleted entry {entry.created_at.date()} - {entry.minutes}', created_by=request.user)
        entry.delete()

    return redirect('dashboard')


@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project.id
    if task.created_by == request.user:
        Logs.objects.create(team=task.team, note=f"Deleted task {task.title}", created_by=request.user)
        task.delete()

    return redirect('project:project_details', project)


@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.created_by == request.user:
        Logs.objects.create(team=project.team, note=f"Deleted project {project.title}", created_by=request.user)
        project.delete()

    return redirect('project:projects')


@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def mark_as_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    task.status = 'done'
    Logs.objects.create(team=task.team, note=f"{task.title} marked as done", created_by=request.user)
    task.save()

    return redirect('project:task_detail', task.project.id, task.id)
