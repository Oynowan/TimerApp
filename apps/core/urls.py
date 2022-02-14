#
# Import Django
from django.urls import path
from django.contrib.auth import views as auth_views

#
# Import Views
from .views import dashboard, signup, reset_pass
from ..project.views import track_entry

#
# Import API views
from ..project.api import api_stop_timer, api_start_timer, api_discard_timer, api_get_tasks, api_get_entries_to_check, api_active_project, api_set_hr
from ..logs.api import api_check_entry
from ..event.api import api_get_events_for_month, api_add_new_event, api_delete_event
from ..password_manager.api import api_get_password_to_clipboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('track_entry/<int:entry_id>/', track_entry, name='track_entry'),
    path('signup/', signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset-password/', reset_pass, name='reset_pass'),



    # API

    path('api/start_timer/', api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api_discard_timer, name='api_discard_timer'),
    path('api/get_tasks/', api_get_tasks, name='api_get_tasks'),
    path('api/check_entry/', api_check_entry, name='api_check_entry'),
    path('api/get_entries/', api_get_entries_to_check, name='api_get_entries_to_check'),
    path('api/active_project/', api_active_project, name="api_active_project"),
    path('api/set_hr/', api_set_hr, name="api_set_hr"),
    path('api/get_events_for_month/', api_get_events_for_month, name="api_get_events_for_month"),
    path('api/add_new_event/', api_add_new_event, name="api_add_new_event"),
    path('api/delete_event/', api_delete_event, name="api_delete_event"),
    path('api/get_password/', api_get_password_to_clipboard, name="api_get_password_to_clipboard"),
]
