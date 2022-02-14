from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .utilities import encryptString
from .models import PasswordStore
from apps.logs.models import Logs
from apps.team.models import Team
from apps.core.decorators import user_passes_test
from apps.core import permissions as per


@login_required
@user_passes_test(per.user_required_group, level='Supervisor')
def password_manager_view(request):
    passwords = PasswordStore.objects.all()
    if request.method == 'POST':
        website = request.POST.get('website')
        username = request.POST.get('username')
        password = request.POST.get('password')
        team = get_object_or_404(Team, pk=request.user.userprofile.team_id)

        password_encrypt = encryptString(password)

        passw = PasswordStore.objects.create(website_name=website, username=username, password=password_encrypt, created_by=request.user)
        Logs.objects.create(team=team, note=f"Account {passw.username} for {passw.website_name} website, was added to manager",
                            created_by=request.user)

    data = {
        'accounts': passwords
    }
    return render(request, 'password_manager/password_manager_view.html', data)

