#
# Import Django
from django.contrib import admin

#
# Import Models
from .models import Team, Invitation

admin.site.register(Team)
admin.site.register(Invitation)