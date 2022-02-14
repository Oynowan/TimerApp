#
# Import Python
import random
import string
from datetime import datetime

#
# Import Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


#
# Import Utilities
from ..emails.utilities import send_invitation_email
from ..core.utilities import get_time_for_user_and_month
from apps.core import permissions as per

#
# Import Models
from .models import Invitation, Team
from ..logs.models import Logs
from ..codes.models import AuthenticationKey

#
# Decorators
from apps.core.decorators import user_passes_test


# Views

@login_required
@user_passes_test(per.user_required_group, level='User')
def list_of_members(request, team_id):
    team = Team.objects.get(pk=team_id)
    members = team.members.all()
    members_list = []
    members_time = []
    for member in members:
        member.time_for_user_and_month = get_time_for_user_and_month(user=member, team=team, date=datetime.now())['total']
        members_time.append(member.time_for_user_and_month)
        if member.last_name:
            members_list.append(f'{member.first_name[0]}.{member.last_name}')
        else:
            members_list.append(member.username)

    if request.user.userprofile.is_ceo or request.user.userprofile.is_hr:
        if request.method == 'POST' and request.user.userprofile.is_ceo:
            email = request.POST.get('email')
            is_ceo = request.POST.get('ceo')
            while True:
                code = ''.join(random.choice(string.ascii_letters + '0123456789') for i in range(30))
                if not AuthenticationKey.objects.filter(key=code):
                    if not User.objects.filter(email=email):
                        authentication = AuthenticationKey.objects.create(key=code)
                        if is_ceo == None:
                            invitation = Invitation.objects.create(auth_key=authentication, email=email, team=team.id)
                        else:
                            invitation = Invitation.objects.create(auth_key=authentication, email=email, team=team.id, is_ceo=is_ceo)
                        send_invitation_email(email, f'?c={code}')

                        Logs.objects.create(team=team, note=f"Invitation sent to {email}", created_by=request.user)

                        messages.info(request, 'Invitation was send')

                        return redirect('list_of_members', team_id)
                    else:

                        messages.info(request, 'Address e-mail already exist in the database')
                        break
    return render(request, 'team/members.html', {'team': team, 'members': members, 'members_time': members_time,
                                                 'members_list': members_list})