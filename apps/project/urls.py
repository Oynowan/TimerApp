#
# Import Django
from django.urls import path

#
# Import Views
from .views import projects, project_details, delete_entry, delete_task, delete_project, task_detail, mark_as_done, \
    add_entry

app_name = 'project'

urlpatterns = [
    path('', projects, name='projects'),
    path('<int:project_id>/', project_details, name='project_details'),
    path('<int:project_id>/<int:task_id>/', task_detail, name="task_detail"),
    path('add_entry/', add_entry, name='add_entry'),
    path('mark_as_done/<int:task_id>/', mark_as_done, name='mark_as_done'),
    path('delete_entry/<int:entry_id>/', delete_entry, name='delete_entry'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
]

