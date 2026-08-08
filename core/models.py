from django.db import models
from django.urls import reverse
from django.utils.text import slugify


EVENT_TYPE_CHOICES = [
    ("wedding", "Wedding"),
    ("engagement", "Engagement"),
    ("birthday", "Birthday party"),
    ("baby_shower", "Baby Shower"),
    ("corporate", "Corprate Event"),
]

BUDGET_RANGE_CHOICES = [
    ("below_50000", "Below-50,000"),
    ("50000_100000", "50,000-100000"),
    ("100000_200000", "100000-200000"),
    ("200000_500000", "200000-500000"),
    ("above_500000", "Above-500000"),
]

LOCATION_CHOICES = [
    ("chennai", "Chennai"),
    ("bangalore", "Bangalore"),
    ("coimbatore", "Coimbatore"),
    ("madurai", "Madurai"),
    ("salem", "Salem"),
]

VENUE_CHOICES = [
    ("banquet_hall", "Banquet Hall"),
    ("convention_center", "Convention Center"),
    ("outdoor_open_ground", "Outdoor / Open Ground"),
    ("beach_resort", "Beach / resort"),
    ("hotel", "Hotel"),
]


class Event(models.Model):
    """A single event listing shown on the Events page and its detail page."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(
        max_length=250, help_text="Shown on cards, e.g. 'A gathering of tech innovators...'"
    )
    description = models.TextField(
        help_text="Longer paragraph shown on the event detail page."
    )
    image = models.ImageField(upload_to="events/")

    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, default="corporate")
    budget_range = models.CharField(max_length=30, choices=BUDGET_RANGE_CHOICES, default="below_50000")
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES, default="chennai")
    venue = models.CharField(max_length=30, choices=VENUE_CHOICES, default="banquet_hall")

    services_included = models.TextField(
        blank=True,
        default="Keynote Speakers\nInteractive Workshops\nNetworking Events\nExhibition Hall",
        help_text="One service per line.",
    )

    highlight_attendees = models.CharField(max_length=50, blank=True, default="500+ Attendees")
    highlight_speakers = models.CharField(max_length=50, blank=True, default="30+ Speakers")
    highlight_duration = models.CharField(max_length=50, blank=True, default="2-Day Event")
    highlight_venue = models.CharField(max_length=80, blank=True, default="Downtown Convention Center")

    pricing_note = models.TextField(
        blank=True,
        default="Pricing varies based on the services selected and the scale of the event. "
        "Contact us for a detailed quote tailored to your specific needs.",
    )

    phone_number = models.CharField(max_length=30, blank=True, default="+1-555-123-4567")

    is_featured = models.BooleanField(
        default=False, help_text="Featured events show up in the homepage Events Preview."
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:event_detail", kwargs={"slug": self.slug})

    @property
    def services_list(self):
        return [line.strip() for line in self.services_included.splitlines() if line.strip()]


class Feature(models.Model):
    """'Our Features' cards on the homepage (Event Planning, Event Design, ...)."""

    ICON_CHOICES = [
        ("calendar", "Calendar"),
        ("palette", "Palette"),
        ("users", "Users"),
        ("megaphone", "Megaphone"),
        ("clock", "Clock"),
        ("wallet", "Wallet"),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="calendar")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class WhyChooseUs(models.Model):
    """'Why Choose Us' cards on the homepage."""

    ICON_CHOICES = [
        ("star", "Star"),
        ("shield", "Shield"),
        ("users", "Users"),
        ("clock", "Clock"),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="star")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why Choose Us Card"
        verbose_name_plural = "Why Choose Us Cards"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date"]

    def __str__(self):
        return f"{self.name} - {self.date}"

    @property
    def stars(self):
        return range(self.rating)


class Service(models.Model):
    """Rows on the Services page (Wedding Planning, Corporate Event Management, ...)."""

    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="team/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class WhyChooseUsAbout(models.Model):
    """The 4 tick-mark cards on the About Us page."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "About - Why Choose Us Card"
        verbose_name_plural = "About - Why Choose Us Cards"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Singleton-style model holding editable site-wide content."""

    site_name = models.CharField(max_length=100, default="Make Events")
    company_name = models.CharField(max_length=100, default="Master Promote")

    hero_title = models.CharField(max_length=200, default="Every Event Memorable & Stress-Free")
    hero_subtitle = models.CharField(
        max_length=300,
        default="We plan, design, and manage unforgettable events with professional execution and creative excellence.",
    )
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)

    about_story = models.TextField(blank=True, default="")
    about_mission = models.TextField(blank=True, default="")
    years_of_experience = models.PositiveIntegerField(default=14)
    about_team_intro = models.TextField(blank=True, default="")

    phone = models.CharField(max_length=30, default="+1-555-123-4567")
    email = models.EmailField(default="info@masterpromote.com")
    office_address = models.CharField(
        max_length=200, default="123 Event Avenue, Cityville, State 12345"
    )

    instagram_url = models.URLField(blank=True, default="#")
    facebook_url = models.URLField(blank=True, default="#")
    twitter_url = models.URLField(blank=True, default="#")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Booking(models.Model):
    """Submissions from the 'Book Your Event' page."""

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    location = models.CharField(max_length=150)
    message = models.TextField(blank=True)
    related_event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, blank=True, null=True, related_name="bookings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_event_type_display()} ({self.event_date})"


class ContactMessage(models.Model):
    """Submissions from the Contact 'Get in touch' page."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
