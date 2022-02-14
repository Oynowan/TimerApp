# Import django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Import Python
import json

# Import decorators
from ..core.decorators import user_passes_test

# Utilities
from apps.core import permissions as per
# Import Models
from ..project.models import Entry
from ..logs.models import Logs
from ..team.models import Team
# API


@login_required
@user_passes_test(per.user_required_group, level='HR')
def api_check_entry(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
    entry_id = json.loads(request.body)['entry_id']
    approve = json.loads(request.body)['approve']
    entry = get_object_or_404(Entry, pk=entry_id)
    entry.checked = True
    entry.approved = approve
    entry.save()
    if approve:
        Logs.objects.create(team=team, note=f"Entry {entry.created_by} - {entry.created_at} - {entry.minutes} "
                                        f"was approved", created_by=request.user)
    else:
        Logs.objects.create(team=team, note=f"Entry {entry.created_by} - {entry.created_at} - {entry.minutes} "
                                        f"was disapproved", created_by=request.user)
    return JsonResponse({'success': True})
