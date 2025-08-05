# events/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('create/', CreateEventView.as_view(), name='create-event'),
    path('event/<int:event_id>/update/', UpdateEventView.as_view(), name='update-event'),
    path('event/<int:event_id>/delete/', DeleteEventView.as_view(), name='delete-event'),
    
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard'),
    path('dashboard/organizer/', OrganizerDashboardView.as_view(), name='organizer_dashboard'),
    path('dashboard/attendee/', AttendeeDashboardView.as_view(), name='attendee-dashboard'),
]
