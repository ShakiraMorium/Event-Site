from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Event
from .forms import EventModelForm 
from django.views.generic import TemplateView 

# Custom mixins for roles
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_attendee(user):
    return user.groups.filter(name='Attendee').exists()

class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_organizer(self.request.user)

class AttendeeRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_attendee(self.request.user)


# Event list view (homepage)
class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    queryset = Event.objects.filter(is_active=True).order_by("start_datetime")[:6]


# Event detail view
class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"
    # pk_url_kwarg = "event_id"


# Create event (organizer only)
class CreateEventView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventModelForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy('event-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['participants_qs'] = self.get_participants_queryset()
        kwargs['categories_qs'] = self.get_categories_queryset()
        return kwargs

    def get_participants_queryset(self):
        return Event.participants.field.related_model.objects.all()

    def get_categories_queryset(self):
        return Event.category.field.related_model.objects.all()

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)


# Update event (organizer only)
class UpdateEventView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = "events/event_form.html"
    pk_url_kwarg = "event_id"
    success_url = reverse_lazy('event-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['participants_qs'] = self.get_participants_queryset()
        kwargs['categories_qs'] = self.get_categories_queryset()
        return kwargs

    def get_participants_queryset(self):
        return Event.participants.field.related_model.objects.all()

    def get_categories_queryset(self):
        return Event.category.field.related_model.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)


# Delete event (organizer only)
class DeleteEventView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    pk_url_kwarg = "event_id"
    success_url = reverse_lazy('event-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully.")
        return super().delete(request, *args, **kwargs)


# Role-based dashboard redirect
class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if is_organizer(request.user):
            return redirect('organizer-dashboard')
        elif is_attendee(request.user):
            return redirect('attendee-dashboard')
        elif request.user.is_superuser:
            return redirect('admin-dashboard')
        return redirect('no-permission')


# Organizer Dashboard
class OrganizerDashboardView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    model = Event
    template_name = "dashboard/organizer_dashboard.html"
    context_object_name = "events"

    def get_queryset(self):
     return Event.objects.filter(organizer=self.request.user).order_by('-start_datetime')
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       events = self.get_queryset()
       now = timezone.now()

       context['total_events'] = events.count()
       context['upcoming_events'] = events.filter(start_datetime__gt=now).count()
       context['completed_events'] = events.filter(end_datetime__lt=now).count()
       return context



# Attendee Dashboard
class AttendeeDashboardView(LoginRequiredMixin, AttendeeRequiredMixin, ListView):
    model = Event
    template_name = "dashboard/attendee_dashboard.html"
    context_object_name = "events"

    def get_queryset(self):
      return Event.objects.filter(participants=self.request.user, is_active=True).order_by('start_datetime')

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       events = self.get_queryset()
       now = timezone.now()
    
       context['total_events'] = events.count()
       context['upcoming_events'] = events.filter(start_datetime__gt=now).count()
       context['completed_events'] = events.filter(end_datetime__lt=now).count()
       return context

# views.py
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Event.objects.all()
        now = timezone.now()
        today = now.date()
        
        context['all_events'] = all_events
        context['today_events'] = all_events.filter(start_datetime__date=today)
        context['upcoming_events'] = all_events.filter(start_datetime__gt=now)
        context['completed_events'] = all_events.filter(end_datetime__lt=now)
        context['total_event_count'] = all_events.count()
        context['completed_event_count'] = context['completed_events'].count()
        context['today_count'] = context['today_events'].count()
        return context