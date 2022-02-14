from django.urls import path

from .views import csv_file, list_of_waiting_entries, all_logs, approve_all_entries

urlpatterns = [
    path('csv_file/<int:user_id>/<int:user_num_months>/', csv_file, name='csv_file'),
    path('waiting_entries/', list_of_waiting_entries, name="waiting_entries"),
    path('waiting_entries/approve_all/', approve_all_entries, name="approve_all_entries"),
    path('', all_logs, name="all_logs")
]