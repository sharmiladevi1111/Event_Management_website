from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Event,
    Feature,
    WhyChooseUs,
    Testimonial,
    Service,
    TeamMember,
    WhyChooseUsAbout,
    EVENT_TYPE_CHOICES,
    BUDGET_RANGE_CHOICES,
    LOCATION_CHOICES,
    VENUE_CHOICES,
)
from .forms import BookingForm, ContactForm


def home(request):
    context = {
        "features": Feature.objects.all(),
        "why_choose_us": WhyChooseUs.objects.all(),
        "featured_events": Event.objects.filter(is_featured=True)[:4] or Event.objects.all()[:4],
        "testimonials": Testimonial.objects.all(),
    }
    return render(request, "core/home.html", context)


def event_list(request):
    events = Event.objects.all()

    event_type = request.GET.get("event_type", "")
    budget_range = request.GET.get("budget_range", "")
    location = request.GET.get("location", "")
    venue = request.GET.get("venue", "")

    if event_type:
        events = events.filter(event_type=event_type)
    if budget_range:
        events = events.filter(budget_range=budget_range)
    if location:
        events = events.filter(location=location)
    if venue:
        events = events.filter(venue=venue)

    context = {
        "events": events,
        "event_type_choices": EVENT_TYPE_CHOICES,
        "budget_range_choices": BUDGET_RANGE_CHOICES,
        "location_choices": LOCATION_CHOICES,
        "venue_choices": VENUE_CHOICES,
        "selected": {
            "event_type": event_type,
            "budget_range": budget_range,
            "location": location,
            "venue": venue,
        },
    }
    return render(request, "core/events.html", context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    context = {"event": event}
    return render(request, "core/event_detail.html", context)


def book_event(request):
    event_slug = request.GET.get("event")
    related_event = None
    if event_slug:
        related_event = Event.objects.filter(slug=event_slug).first()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if related_event:
                booking.related_event = related_event
            booking.save()
            messages.success(
                request,
                "Your booking request has been submitted! We'll get back to you within 24 hours.",
            )
            return redirect("core:book_event")
    else:
        initial = {}
        if related_event:
            initial["event_type"] = related_event.event_type
        form = BookingForm(initial=initial)

    context = {"form": form, "related_event": related_event}
    return render(request, "core/book_event.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We'll respond shortly.")
            return redirect("core:contact")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})


def services(request):
    return render(request, "core/services.html", {"services": Service.objects.all()})


def about(request):
    context = {
        "team_members": TeamMember.objects.all(),
        "why_choose_us_about": WhyChooseUsAbout.objects.all(),
    }
    return render(request, "core/about.html", context)
