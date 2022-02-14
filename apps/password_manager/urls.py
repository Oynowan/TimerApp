from django.urls import path

from .views import password_manager_view

urlpatterns = [
    path('', password_manager_view, name="password_manager_view"),
]