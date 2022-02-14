#
# Import Python
import json
from datetime import datetime, timezone, timedelta
from django.core.checks import messages
#
# Import Django
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#
# Import Models
from .models import Event
from ..logs.models import Logs
from ..team.models import Team

# API View

@login_required
def api_get_events_for_month(request):
    events_array = []
    month = json.loads(request.body)['month']
    year = json.loads(request.body)['year']

    events = Event.objects.filter(date__month=month, date__year=year)
    for event in events:
        user_name = ''

        if event.user.first_name != '':
            user_name = event.user.first_name + ' ' + event.user.last_name
        else:
            user_name = event.user.username
        obj = {
            'id': event.id,
            'user': user_name,
            'user_id': event.user.id,
            'title': event.title,
            'date': event.date,
            'start_date': event.start_date,
            'last_date': event.last_date,
            'day': event.date.day,
            'bussy': event.bussy,
            'parent': event.parent,
            'child': event.child,
            'longer': event.longer_time,
            'time': event.minutes,
            'last_day': event.last_event_day
        }
        events_array.append(obj)
    return JsonResponse({'message': 'success', 'events': events_array})


@login_required
def api_add_new_event(request):

    user = request.user

    if Event.objects.filter(user=user):
        return JsonResponse({'message': 'error'})

    text = json.loads(request.body)['text']
    bussy = json.loads(request.body)['bussy']
    date = json.loads(request.body)['date']
    durration = json.loads(request.body)['durration']

    date_array = date.split('-')
    date_ = datetime(int(date_array[0]), int(date_array[1]), int(date_array[2]))
    
    team = get_object_or_404(Team, pk=user.userprofile.team_id)
    month = date_.month
    start_date = date_.date()

    events_back = []
    longer = False
    last_date = date_
    if int(durration) > 1:
        longer = True
        last_date = date_ + timedelta(days=int(durration)-1)

    event = Event.objects.create(user=user, title=text, bussy=bussy, date=date_.date(), start_date=start_date, longer_time=longer, last_date=last_date.date(), minutes=durration)
    event_id = event.id
    user_name = ''


    Logs.objects.create(team=team, note=f"New event '{event.title}' was created",
                            created_by=user)

    if event.user.first_name != '':
        user_name = event.user.first_name + ' ' + event.user.last_name
    else:
        user_name = event.user.username
    obj = {
            'id': event.id,
            'user': user_name,
            'user_id': event.user.id,
            'title': event.title,
            'date': event.date,
            'start_date': event.start_date,
            'last_date': event.last_date,
            'day': event.date.day,
            'bussy': event.bussy,
            'parent': event.parent,
            'child': event.child,
            'longer': event.longer_time,
            'time': event.minutes,
            'last_day': event.last_event_day
        }
    events_back.append(obj)

    if int(durration) > 1:
        title = text + ' longer'
        for durr in range(1,int(durration)):
            last_day = False
            if durr+1 == int(durration):
                last_day = True
            date_ = date_+ timedelta(days=1)
            event = Event.objects.create(user=user, title=text, bussy=bussy, date=date_.date(), start_date=start_date, longer_time=longer, parent=False, parent_id=event_id, 
                                        last_date=last_date.date(), minutes=durration, child=True, last_event_day=last_day)
            user_name = ''

            if event.user.first_name != '':
                user_name = event.user.first_name + ' ' + event.user.last_name
            else:
                user_name = event.user.username
            if event.date.month == month:
                obj = {
                    'id': event.id,
                    'user': user_name,
                    'user_id': event.user.id,
                    'title': event.title,
                    'date': event.date,
                    'start_date': event.start_date,
                    'last_date': event.last_date,
                    'day': event.date.day,
                    'bussy': event.bussy,
                    'parent': event.parent,
                    'child': event.child,
                    'longer': event.longer_time,
                    'time': event.minutes,
                    'last_day': event.last_event_day

                }
                events_back.append(obj)
    

    return JsonResponse({'message': 'success', 'events': events_back})


@login_required
def api_delete_event(request):
    event_id = json.loads(request.body)['event_id']
    user = request.user
    event = get_object_or_404(Event, pk=event_id)
    team = get_object_or_404(Team, pk=user.userprofile.team_id)
    if event.user == user:
        title = event.title
        if event.longer_time and event.parent:
            events = Event.objects.filter(parent_id=event.id)
            event.delete()
            for event in events:
                event.delete()

        elif event.longer_time and not event.parent:
            event_parent = get_object_or_404(Event, pk=event.parent_id)
            events = Event.objects.filter(parent_id=event.parent_id)
            event_parent.delete()
            for event in events:
                event.delete()

        else:
            event.delete()

        Logs.objects.create(team=team, note=f"Event '{event.title}' was deleted",
                            created_by=user)

        data = {
            'message': 'success'
        }
    else:
        data={
            'message': 'Not allowed to delete'
        }
    
    return JsonResponse(data)
