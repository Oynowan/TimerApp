"""bv_timer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from apps.core.views import signup


urlpatterns = [
    path('admin/', admin.site.urls),

    # Core
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login_'),
    path('', include('apps.core.urls')),

    # Account
    path('account/', include('apps.userprofile.urls')),

    # Password
    path('accounts/', include('django.contrib.auth.urls')),

    # Team
    path('members/', include('apps.team.urls')),

    # Project
    path('projects/', include('apps.project.urls')),

    # Logs
    path('logs/', include('apps.logs.urls')),

    # PasswordManager
    path('pm/', include('apps.password_manager.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'