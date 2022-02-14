from django.db import models
from django.contrib.auth.models import User
from .utilities import decryptString

class PasswordStore(models.Model):

    website_name = models.CharField(max_length=255, verbose_name='Name of the website')
    username= models.CharField(max_length=255, verbose_name='Username used to log in')
    password = models.CharField(max_length=255, verbose_name='Password used to log in')
    created_by = models.ForeignKey(User, verbose_name="Created by user", on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.website_name} => {self.username}'
    
    def get_password(self):
        return decryptString(str.encode(self.password))
