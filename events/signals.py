# events/signals.py

from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_event_assignment(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [p.email for p in instance.participants.all()]
        send_mail(
            "You're Invited to an Event!",
            f"You've been added to the event: {instance.title}",
            "eventorganizer@example.com",  # Update with your sender email
            assigned_emails,
            fail_silently=False,
        )


@receiver(post_delete, sender=Event)
def delete_event_related_objects(sender, instance, **kwargs):
    # If you later add an EventDetail model linked to Event via OneToOne or FK
    if hasattr(instance, 'details'):
        instance.details.delete()
