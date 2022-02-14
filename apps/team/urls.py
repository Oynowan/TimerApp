#
# Import Django

from django.urls import path

from .views import list_of_members

urlpatterns = [
    path('<int:team_id>/', list_of_members, name='list_of_members'),
]