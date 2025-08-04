from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.conf import settings



class Group(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Participant(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
    



class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='events/images/', blank=True, null=True)
    category = models.ForeignKey(Category,related_name="events", on_delete=models.CASCADE,)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime =  models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField( Participant,related_name="events",blank=True,)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 
    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        return self.title
    
   

    @property
    def participants_count(self):
        """Quick helper for templates/admin."""
        return self.participants.count()

   