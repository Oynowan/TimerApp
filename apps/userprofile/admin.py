from django.contrib import admin

# Register your models here.
from .models import Userprofile, ResetPassword

admin.site.register(Userprofile),
admin.site.register(ResetPassword)
