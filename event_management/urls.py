"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from core.views import home,no_permission
from events.views import EventListView
from django.views.generic import TemplateView 
from debug_toolbar.toolbar import  debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    # path("cores/", include("core.urls")),
    path("events/", include("events.urls")),
    path('', EventListView.as_view(), name='home'),
    path("users/", include("users.urls",namespace="users")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('no-permission/', TemplateView.as_view(template_name="no_permission.html"), name='no-permission'),
]+ debug_toolbar_urls()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

