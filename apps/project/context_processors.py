#
# Import Python
from datetime import datetime, timezone

#
# Import Django
from django.shortcuts import get_object_or_404

#
# Import models
from .models import Entry
from ..team.models import Team


# Context Processors

def active_entry(request):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk=request.user.userprofile.team_id)
        untracked_entries = Entry.objects.filter(team=team, created_by=request.user, minutes=0, is_tracked=False)

        if untracked_entries:
            active_entry = untracked_entries.first()
            active_entry.second_since = int((datetime.now(timezone.utc) - active_entry.created_at).total_seconds())
            entry_id = active_entry.id
            set_minutes = active_entry.set_minutes

            return {'active_entry_seconds': active_entry.second_since, 'start_time': active_entry.created_at.isoformat(),
                    'entry_id': entry_id, 'set_minutes': set_minutes}
    entry_id = 0
    return {'active_entry_seconds': 0, 'start_time': datetime.now().isoformat(), 'entry_id': entry_id, 'set_minutes': 1}
