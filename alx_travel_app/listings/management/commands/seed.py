import random
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from alx_travel_app.listings.models import Listing, Booking, Review

CITIES = [
    ("Lagos", "Nigeria"), ("Abuja", "Nigeria"), ("Accra", "Ghana"),
    ("Nairobi", "Kenya"), ("Cairo", "Egypt"), ("Cape Town", "South Africa"),
    ("Kigali", "Rwanda"),
]
TITLES = [
    "Cozy Studio", "Beachfront Apartment", "City Center Loft",
    "Quiet Suburban Home", "Modern Condo", "Charming Bungalow", "Mountain View Cabin",
]
REV_COMMENTS = [
    "Great place, very clean!", "Host was responsive and helpful.",
    "Amazing location, will book again.", "Decent stay for the price.",
    "Could be cleaner, but overall okay.", "Loved it—highly recommended!",
]

class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--listings", type=int, default=10, help="Number of listings to create")
        parser.add_argument("--purge", action="store_true", help="Delete existing data before seeding")

    @transaction.atomic
    def handle(self, *args, **options):
        n_listings = options["listings"]
        purge = options["purge"]

        if purge:
            self.stdout.write(self.style.WARNING("Purging existing data..."))
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()

        self.stdout.write(self.style.MIGRATE_HEADING(f"Seeding {n_listings} listings..."))
        created_listings = []

        for i in range(n_listings):
            city, country = random.choice(CITIES)
            title = random.choice(TITLES)
            price = Decimal(random.randrange(25, 200))
            max_guests = random.randint(1, 6)
            listing = Listing.objects.create(
                title=f"{title} #{i+1}",
                description="Auto-seeded listing for development/testing.",
                city=city, country=country,
                price_per_night=price, max_guests=max_guests, is_active=True,
            )
            created_listings.append(listing)

        for listing in created_listings:
            for _ in range(random.randint(1, 3)):
                Review.objects.create(
                    listing=listing,
                    reviewer_name=random.choice(["Ada","Tunde","Wale","Aisha","Kwame","Zainab"]),
                    rating=random.randint(3, 5),
                    comment=random.choice(REV_COMMENTS),
                )

            today = date.today()
            base_start = today + timedelta(days=random.randint(1, 20))
            for _ in range(random.randint(1, 3)):
                start = base_start + timedelta(days=random.randint(0, 20))
                nights = random.randint(1, 5)
                end = start + timedelta(days=nights)
                guests = random.randint(1, max(1, listing.max_guests))
                Booking.objects.create(
                    listing=listing,
                    guest_name=random.choice(["Emeka","Bola","Kunle","Sade","Joseph","Ngozi"]),
                    guests=guests, start_date=start, end_date=end, status="CONFIRMED",
                )

        self.stdout.write(self.style.SUCCESS("Seeding completed."))
