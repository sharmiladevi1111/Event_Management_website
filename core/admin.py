from django.contrib import admin
from .models import (
    Event,
    Feature,
    WhyChooseUs,
    Testimonial,
    Service,
    TeamMember,
    WhyChooseUsAbout,
    SiteSettings,
    Booking,
    ContactMessage,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "location", "venue", "budget_range", "is_featured", "order")
    list_filter = ("event_type", "location", "venue", "budget_range", "is_featured")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "order")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "rating", "order")
    list_editable = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


@admin.register(WhyChooseUsAbout)
class WhyChooseUsAboutAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "event_date", "location", "phone_number", "is_handled", "created_at")
    list_filter = ("event_type", "is_handled")
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "phone_number", "location")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "is_handled", "created_at")
    list_filter = ("is_handled",)
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "subject")
