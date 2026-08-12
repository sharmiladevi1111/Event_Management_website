import datetime
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking, ContactMessage, EVENT_TYPE_CHOICES

# Accepts optional leading +, then 7-15 digits, with optional spaces/hyphens
# in between (e.g. "+91 93604 65756", "9360465756", "555-123-4567").
PHONE_REGEX = re.compile(r"^\+?[0-9][0-9\s\-]{6,17}[0-9]$")


def validate_phone(value):
    cleaned = value.strip()
    if not PHONE_REGEX.match(cleaned):
        raise ValidationError(
            "Enter a valid phone number (7-15 digits, optionally starting with +)."
        )
    digit_count = len(re.sub(r"\D", "", cleaned))
    if digit_count < 7 or digit_count > 15:
        raise ValidationError("Phone number must have between 7 and 15 digits.")
    return cleaned


def validate_person_name(value):
    cleaned = value.strip()
    if len(cleaned) < 2:
        raise ValidationError("Name must be at least 2 characters long.")
    if not re.match(r"^[A-Za-z\s.'\-]+$", cleaned):
        raise ValidationError("Name can only contain letters, spaces, and . ' -")
    return cleaned


class BookingForm(forms.ModelForm):
    event_type = forms.ChoiceField(
        choices=[("", "Select event type")] + EVENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        error_messages={"required": "Please select an event type."},
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
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                    "minlength": "2",
                    "autocomplete": "name",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                    "inputmode": "tel",
                    "autocomplete": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                    "autocomplete": "email",
                }
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Stop the browser's native date picker from offering past dates.
        today = timezone.localdate().isoformat()
        self.fields["event_date"].widget.attrs["min"] = today

    def clean_name(self):
        return validate_person_name(self.cleaned_data["name"])

    def clean_phone_number(self):
        return validate_phone(self.cleaned_data["phone_number"])

    def clean_location(self):
        cleaned = self.cleaned_data["location"].strip()
        if len(cleaned) < 2:
            raise ValidationError("Please enter a valid location.")
        return cleaned

    def clean_event_date(self):
        event_date = self.cleaned_data["event_date"]
        if event_date < timezone.localdate():
            raise ValidationError("Event date can't be in the past — please pick a future date.")
        max_date = timezone.localdate() + datetime.timedelta(days=5 * 365)
        if event_date > max_date:
            raise ValidationError("That date is too far in the future — please pick within 5 years.")
        return event_date


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your name", "minlength": "2"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your email"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your phone number",
                    "inputmode": "tel",
                }
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Subject", "minlength": "3"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your message",
                    "rows": 5,
                    "minlength": "10",
                }
            ),
        }

    def clean_name(self):
        return validate_person_name(self.cleaned_data["name"])

    def clean_phone(self):
        value = self.cleaned_data.get("phone", "").strip()
        if not value:
            return value  # phone is optional on the contact form
        return validate_phone(value)

    def clean_subject(self):
        cleaned = self.cleaned_data["subject"].strip()
        if len(cleaned) < 3:
            raise ValidationError("Subject must be at least 3 characters long.")
        return cleaned

    def clean_message(self):
        cleaned = self.cleaned_data["message"].strip()
        if len(cleaned) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return cleaned