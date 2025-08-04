import os
import django
from faker import Faker
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_site.settings')  
django.setup()

from events.models import Category, Event, Participant

def populate_db():
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
    name=fake.word().capitalize()
  ) for _ in range(5)]
    
    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f" Created {len(participants)} participants.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            title=fake.catch_phrase(),
            description=fake.paragraph(),
            category=random.choice(categories),
            date=fake.date_time_this_year(),
            location=fake.city(),
            is_public=random.choice([True, False])
        )
        # Assign participants randomly
        event.participants.set(random.sample(participants, random.randint(1, 5)))
        events.append(event)
    print(f"Created {len(events)} events with participants.")

    print(" Database populated successfully!")

if __name__ == '__main__':
    populate_db()
