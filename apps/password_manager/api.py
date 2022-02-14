from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PasswordStore
from apps.core.decorators import ceo_member_required
from apps.emails.utilities import password_manager_email
import json
from apps.core.decorators import user_passes_test
from apps.core import permissions as per


@user_passes_test(per.user_required_group, level='Supervisor')
def api_get_password_to_clipboard(request):
    pass_id = json.loads(request.body)['pass_id']
    user = request.user
    password = get_object_or_404(PasswordStore, pk=pass_id)

    password_manager_email(request.user.username, password)

    return JsonResponse({'message': 'success'})