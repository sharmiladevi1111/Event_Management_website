from django import forms
from .models import Booking, ContactMessage, EVENT_TYPE_CHOICES


class BookingForm(forms.ModelForm):
    event_type = forms.ChoiceField(
        choices=[("", "Select event type")] + EVENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Booking
        fields = [
            "name",
            "phone_number",
            "email",
            "event_type",
            "event_date",
            "location",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your phone number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "event_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "placeholder": "Select event date"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event location"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell us more about your requirements",
                    "rows": 5,
                }
            ),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your phone number"}
            ),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Your message", "rows": 5}
            ),
        }
