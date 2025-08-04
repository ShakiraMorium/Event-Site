from django import forms
from .models import Event, Category, Participant
from django.conf import settings


class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "type": "datetime-local"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 
            'description', 
            'image', 
            'category', 
            'organizer', 
            'start_datetime', 
            'end_datetime', 
            'participants',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'participants': forms.CheckboxSelectMultiple,
            'organizer': forms.HiddenInput(),  # hide organizer input, set programmatically
        }

    def __init__(self, *args, **kwargs):
        participants_qs = kwargs.pop('participants_qs', Participant.objects.all())
        categories_qs = kwargs.pop('categories_qs', Category.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = participants_qs
        self.fields['category'].queryset = categories_qs
