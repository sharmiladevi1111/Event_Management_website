from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("events/", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("book-event/", views.book_event, name="book_event"),
    path("contact/", views.contact, name="contact"),
    path("services/", views.services, name="services"),
    path("about-us/", views.about, name="about"),
]
