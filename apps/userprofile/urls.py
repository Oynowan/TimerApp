#
# Import Django

from django.urls import path

#
# Import Views
from .views import myaccount, edit_profile, users_profile, reset_password

urlpatterns = [
    path('myaccount/', myaccount, name='myaccount'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user/<int:user_id>/', users_profile, name='users_profile'),
    path('myaccount/reset-password/', reset_password, name='reset-password'),
]