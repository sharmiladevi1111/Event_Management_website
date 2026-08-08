import datetime
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import (
    Event,
    Feature,
    WhyChooseUs,
    Testimonial,
    Service,
    TeamMember,
    WhyChooseUsAbout,
    SiteSettings,
)

SEED_DIR = os.path.join(settings.BASE_DIR, "seed_images")


def attach_image(field, path):
    with open(path, "rb") as f:
        field.save(os.path.basename(path), File(f), save=False)


class Command(BaseCommand):
    help = "Populate the database with sample data matching the Make Events prototype."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing seeded content before re-creating it.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            Event.objects.all().delete()
            Feature.objects.all().delete()
            WhyChooseUs.objects.all().delete()
            Testimonial.objects.all().delete()
            Service.objects.all().delete()
            TeamMember.objects.all().delete()
            WhyChooseUsAbout.objects.all().delete()
            self.stdout.write("Cleared existing seed content.")

        self.seed_site_settings()
        self.seed_features()
        self.seed_why_choose_us()
        self.seed_events()
        self.seed_testimonials()
        self.seed_services()
        self.seed_team()
        self.seed_about_why_choose_us()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

    def seed_site_settings(self):
        s = SiteSettings.load()
        s.site_name = "Make Events"
        s.company_name = "Master Promote"
        s.hero_title = "Every Event Memorable & Stress-Free"
        s.hero_subtitle = (
            "We plan, design, and manage unforgettable events with professional "
            "execution and creative excellence."
        )
        if not s.hero_image:
            attach_image(s.hero_image, os.path.join(SEED_DIR, "hero.jpg"))
        s.about_story = (
            "Founded in 2010, MASTER PROMOTE began as a small team of passionate event "
            "planners with a vision to transform ordinary gatherings into extraordinary "
            "experiences. Over the years, we've grown into a leading event management "
            "company, known for our creativity, attention to detail, and commitment to "
            "client satisfaction. Our journey has been marked by countless successful "
            "events, ranging from intimate celebrations to large-scale corporate "
            "functions, each reflecting our dedication to excellence."
        )
        s.about_mission = (
            "Our mission is to craft exceptional events that exceed expectations and "
            "leave a lasting impression. We envision a world where every event is a "
            "seamless, memorable experience, meticulously planned and flawlessly "
            "executed. We strive to be the premier choice for event management, "
            "recognized for our innovative approach, personalized service, and "
            "unwavering commitment to quality."
        )
        s.years_of_experience = 14
        s.about_team_intro = (
            "Our team is composed of seasoned professionals with diverse backgrounds "
            "in event planning, design, logistics, and marketing. Each member brings "
            "a unique set of skills and expertise, united by a shared passion for "
            "creating exceptional events. We foster a collaborative environment where "
            "creativity thrives, and every event benefits from our collective "
            "knowledge and experience."
        )
        s.phone = "+1-555-123-4567"
        s.email = "info@masterpromote.com"
        s.office_address = "123 Event Avenue, Cityville, State 12345"
        s.save()
        self.stdout.write("Site settings ready.")

    def seed_features(self):
        data = [
            ("calendar", "Event Planning", "Comprehensive planning from concept to execution."),
            ("palette", "Event Design", "Creative design to match your vision."),
            ("users", "Guest Management", "Seamless management of guest lists and RSVPs."),
            ("megaphone", "Promotion & Marketing", "Effective marketing to maximize attendance."),
            ("clock", "On-Site Coordination", "Professional coordination on the day of the event."),
            ("wallet", "Budget Management", "Efficient budget management to ensure cost-effectiveness."),
        ]
        for i, (icon, title, desc) in enumerate(data):
            Feature.objects.update_or_create(
                title=title, defaults={"icon": icon, "description": desc, "order": i}
            )
        self.stdout.write("Features ready.")

    def seed_why_choose_us(self):
        data = [
            ("star", "Proven Expertise", "Years of experience delivering exceptional events."),
            ("shield", "Reliable Service", "Dependable service you can trust."),
            ("users", "Client-Centric Approach", "Tailored solutions to meet your specific needs."),
            ("clock", "Time-Saving Solutions", "Efficient planning to save you time and effort."),
        ]
        for i, (icon, title, desc) in enumerate(data):
            WhyChooseUs.objects.update_or_create(
                title=title, defaults={"icon": icon, "description": desc, "order": i}
            )
        self.stdout.write("Why Choose Us cards ready.")

    def seed_events(self):
        events = [
            dict(
                title="Tech Conference 2024",
                short_description="A gathering of tech innovators and industry leaders.",
                description=(
                    "Join us for the Tech Conference 2024, a leading event for technology "
                    "professionals, innovators, and enthusiasts. This conference will feature "
                    "keynote speeches from industry leaders, interactive workshops, and "
                    "networking opportunities. Explore the latest advancements in AI, "
                    "cybersecurity, cloud computing, and more. Engage with experts, discover "
                    "new solutions, and connect with peers to drive your career and business "
                    "forward."
                ),
                image="tech_conference_2024.jpg",
                event_type="corporate",
                budget_range="200000_500000",
                location="chennai",
                venue="convention_center",
                services_included="Keynote Speakers\nInteractive Workshops\nNetworking Events\nExhibition Hall",
                highlight_attendees="500+ Attendees",
                highlight_speakers="30+ Speakers",
                highlight_duration="2-Day Event",
                highlight_venue="Downtown Convention Center",
                is_featured=True,
            ),
            dict(
                title="Corporate Events",
                short_description="Professional and impactful corporate gatherings.",
                description=(
                    "From product launches to annual conferences, we design corporate events "
                    "that align with your brand and business objectives, handling every "
                    "detail from venue sourcing to attendee engagement."
                ),
                image="corporate_events.jpg",
                event_type="corporate",
                budget_range="100000_200000",
                location="bangalore",
                venue="convention_center",
                highlight_attendees="300+ Attendees",
                highlight_speakers="15+ Speakers",
                highlight_duration="1-Day Event",
                highlight_venue="City Business Hub",
                is_featured=True,
            ),
            dict(
                title="Private Parties",
                short_description="Memorable and fun private parties.",
                description=(
                    "Celebrate your special moments with a personalized party planning "
                    "service covering theme development, catering, entertainment, and decor."
                ),
                image="private_parties.jpg",
                event_type="birthday",
                budget_range="50000_100000",
                location="coimbatore",
                venue="banquet_hall",
                highlight_attendees="50+ Guests",
                highlight_speakers="Live DJ",
                highlight_duration="1 Evening",
                highlight_venue="Private Banquet Hall",
                is_featured=True,
            ),
            dict(
                title="Festivals",
                short_description="Large-scale music and arts festivals.",
                description=(
                    "We produce large-scale music and arts festivals, managing stage design, "
                    "vendor coordination, ticketing, and crowd experience from start to finish."
                ),
                image="festivals.jpg",
                event_type="corporate",
                budget_range="above_500000",
                location="madurai",
                venue="outdoor_open_ground",
                highlight_attendees="5000+ Attendees",
                highlight_speakers="20+ Performers",
                highlight_duration="3-Day Event",
                highlight_venue="Open Ground Arena",
                is_featured=True,
            ),
            dict(
                title="Weddings",
                short_description="Elegant and personalized wedding celebrations.",
                description=(
                    "Our wedding planning service is designed to create a seamless and "
                    "unforgettable experience for you and your guests, from venue selection "
                    "and vendor coordination to day-of logistics."
                ),
                image="weddings.jpg",
                event_type="wedding",
                budget_range="200000_500000",
                location="salem",
                venue="hotel",
                highlight_attendees="250+ Guests",
                highlight_speakers="Live Band",
                highlight_duration="2-Day Celebration",
                highlight_venue="Luxury Hotel Ballroom",
            ),
            dict(
                title="Summer Music Festival",
                short_description="An outdoor celebration of music and community.",
                description=(
                    "An outdoor celebration of music and community featuring local and "
                    "touring artists across multiple stages with food trucks and art "
                    "installations."
                ),
                image="summer_music_festival.jpg",
                event_type="corporate",
                budget_range="above_500000",
                location="chennai",
                venue="outdoor_open_ground",
                highlight_attendees="3000+ Attendees",
                highlight_speakers="12+ Artists",
                highlight_duration="2-Day Event",
                highlight_venue="Riverside Grounds",
            ),
            dict(
                title="Corporate Gala Night",
                short_description="An elegant evening for networking and recognition.",
                description=(
                    "An elegant evening of networking and recognition, complete with a "
                    "formal dinner, awards ceremony, and live entertainment for your team "
                    "and partners."
                ),
                image="corporate_gala_night.jpg",
                event_type="corporate",
                budget_range="200000_500000",
                location="bangalore",
                venue="hotel",
                highlight_attendees="400+ Guests",
                highlight_speakers="Awards Ceremony",
                highlight_duration="1 Evening",
                highlight_venue="Grand Hotel Ballroom",
            ),
            dict(
                title="Art Exhibition Opening",
                short_description="Showcasing contemporary art from emerging artists.",
                description=(
                    "Showcasing contemporary art from emerging artists, complete with "
                    "curated gallery walkthroughs, artist talks, and an opening night "
                    "reception."
                ),
                image="art_exhibition_opening.jpg",
                event_type="corporate",
                budget_range="50000_100000",
                location="coimbatore",
                venue="convention_center",
                highlight_attendees="200+ Guests",
                highlight_speakers="10+ Artists",
                highlight_duration="1 Evening",
                highlight_venue="Modern Art Gallery",
            ),
            dict(
                title="Charity Auction Event",
                short_description="Raising funds for a noble cause with exclusive items.",
                description=(
                    "Raising funds for a noble cause with exclusive auction items, a formal "
                    "dinner program, and a dedicated fundraising strategy."
                ),
                image="charity_auction_event.jpg",
                event_type="corporate",
                budget_range="100000_200000",
                location="madurai",
                venue="banquet_hall",
                highlight_attendees="150+ Guests",
                highlight_speakers="Guest Auctioneer",
                highlight_duration="1 Evening",
                highlight_venue="Grand Banquet Hall",
            ),
            dict(
                title="Food & Wine Tasting",
                short_description="A culinary journey with fine wines and gourmet dishes.",
                description=(
                    "A curated culinary journey pairing fine wines with gourmet dishes from "
                    "renowned local chefs, in an intimate outdoor setting."
                ),
                image="food_and_wine_tasting.jpg",
                event_type="corporate",
                budget_range="50000_100000",
                location="salem",
                venue="outdoor_open_ground",
                highlight_attendees="80+ Guests",
                highlight_speakers="5+ Chefs",
                highlight_duration="1 Evening",
                highlight_venue="Garden Terrace",
            ),
            dict(
                title="Name Ceremony",
                short_description="Memorable and fun private parties.",
                description=(
                    "A warm, personalized naming ceremony celebration with traditional "
                    "decor, catering, and photography to mark the special day."
                ),
                image="name_ceremony.jpg",
                event_type="baby_shower",
                budget_range="below_50000",
                location="chennai",
                venue="banquet_hall",
                highlight_attendees="100+ Guests",
                highlight_speakers="Traditional Rituals",
                highlight_duration="Half Day",
                highlight_venue="Community Banquet Hall",
            ),
            dict(
                title="Baby Shower",
                short_description="Large-scale music and arts festivals.",
                description=(
                    "A joyful baby shower celebration with custom themes, decor, games, and "
                    "catering tailored to the parents-to-be."
                ),
                image="baby_shower.jpg",
                event_type="baby_shower",
                budget_range="below_50000",
                location="bangalore",
                venue="banquet_hall",
                highlight_attendees="60+ Guests",
                highlight_speakers="Themed Decor",
                highlight_duration="Half Day",
                highlight_venue="Private Hall",
            ),
        ]

        for i, data in enumerate(events):
            image_name = data.pop("image")
            event, created = Event.objects.update_or_create(
                title=data["title"], defaults={**data, "order": i}
            )
            if created or not event.image:
                attach_image(event.image, os.path.join(SEED_DIR, "events", image_name))
                event.save()
        self.stdout.write("Events ready.")

    def seed_testimonials(self):
        data = [
            (
                "Sophia Carter",
                datetime.date(2024, 5, 15),
                5,
                "Master Promote made our wedding day absolutely perfect. Their attention "
                "to detail and seamless execution allowed us to fully enjoy our special "
                "day without any stress. Highly recommend!",
                "sophia_carter.jpg",
            ),
            (
                "Ethan Bennett",
                datetime.date(2024, 4, 22),
                5,
                "We hired Master Promote for our annual corporate conference, and they "
                "exceeded our expectations. The event was well-organized, professional, "
                "and received rave reviews from our attendees.",
                "ethan_bennett.jpg",
            ),
            (
                "Olivia Hayes",
                datetime.date(2024, 3, 10),
                5,
                "Master Promote planned my 50th birthday party, and it was a huge "
                "success. The team was creative, responsive, and made sure every detail "
                "was perfect. I couldn't have asked for a better experience.",
                "olivia_hayes.jpg",
            ),
        ]
        for i, (name, date, rating, message, image) in enumerate(data):
            t, created = Testimonial.objects.update_or_create(
                name=name, defaults={"date": date, "rating": rating, "message": message, "order": i}
            )
            if created or not t.avatar:
                attach_image(t.avatar, os.path.join(SEED_DIR, "testimonials", image))
                t.save()
        self.stdout.write("Testimonials ready.")

    def seed_services(self):
        data = [
            (
                "Wedding Planning",
                "Our wedding planning service is designed to create a seamless and "
                "unforgettable experience for you and your guests. We handle every "
                "aspect, from venue selection and vendor coordination to day-of logistics "
                "and post-event follow-up. Our goal is to bring your vision to life, "
                "ensuring your special day is as magical and stress-free as possible.",
            ),
            (
                "Corporate Event Management",
                "We specialize in managing corporate events that align with your business "
                "objectives. Whether it's a conference, seminar, product launch, or "
                "team-building retreat, we provide end-to-end solutions, including venue "
                "sourcing, speaker management, and attendee engagement strategies. Our "
                "focus is on delivering impactful events that enhance your brand and "
                "foster meaningful connections.",
            ),
            (
                "Birthday & Private Parties",
                "Celebrate your special moments with our personalized party planning "
                "service. We cater to all types of private events, from intimate birthday "
                "gatherings to lavish anniversary celebrations. Our services include theme "
                "development, catering, entertainment, and decor, ensuring your party is a "
                "reflection of your style and a memorable experience for all attendees.",
            ),
            (
                "Cultural & Stage Programs",
                "We bring creativity and precision to cultural and stage programs, "
                "managing everything from talent acquisition and stage design to "
                "technical production and audience engagement. Whether it's a theatrical "
                "performance, music concert, or cultural festival, we ensure a captivating "
                "and well-executed event that leaves a lasting impression.",
            ),
        ]
        for i, (title, desc) in enumerate(data):
            Service.objects.update_or_create(
                title=title, defaults={"description": desc, "order": i}
            )
        self.stdout.write("Services ready.")

    def seed_team(self):
        data = [
            ("Emily Carter", "Lead Event Planner", "emily_carter.jpg"),
            ("David Lee", "Creative Director", "david_lee.jpg"),
            ("Sophia Clark", "Logistics Manager", "sophia_clark.jpg"),
        ]
        for i, (name, role, image) in enumerate(data):
            member, created = TeamMember.objects.update_or_create(
                name=name, defaults={"role": role, "order": i}
            )
            if created or not member.photo:
                attach_image(member.photo, os.path.join(SEED_DIR, "team", image))
                member.save()
        self.stdout.write("Team ready.")

    def seed_about_why_choose_us(self):
        data = [
            (
                "Expertise and Experience",
                "With over 14 years in the industry, we have the knowledge and skills to "
                "handle events of any size and complexity.",
            ),
            (
                "Personalized Service",
                "We take the time to understand your unique needs and preferences, "
                "tailoring our services to create a truly personalized experience.",
            ),
            (
                "Attention to Detail",
                "From the smallest details to the grandest gestures, we ensure every "
                "aspect of your event is perfect.",
            ),
            (
                "Proven Track Record",
                "Our portfolio of successful events speaks for itself, demonstrating our "
                "commitment to delivering exceptional results.",
            ),
        ]
        for i, (title, desc) in enumerate(data):
            WhyChooseUsAbout.objects.update_or_create(
                title=title, defaults={"description": desc, "order": i}
            )
        self.stdout.write("About page 'Why Choose Us' cards ready.")
