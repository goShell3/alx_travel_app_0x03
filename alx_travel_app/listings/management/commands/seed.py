from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create sample users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'user{i+1}',
                email=f'user{i+1}@example.com',
                password='password123',
                first_name=f'First{i+1}',
                last_name=f'Last{i+1}'
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Create sample listings
        locations = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
        amenities = [
            ['WiFi', 'Kitchen', 'Pool'],
            ['WiFi', 'Gym', 'Parking'],
            ['WiFi', 'Air Conditioning', 'Washer'],
            ['WiFi', 'TV', 'Heating'],
            ['WiFi', 'Elevator', 'Security']
        ]
        
        listings = []
        for i in range(10):
            host = random.choice(users)
            listing = Listing.objects.create(
                title=f'Beautiful {locations[i % len(locations)]} Apartment',
                description=f'Luxurious apartment in the heart of {locations[i % len(locations)]}',
                price=random.randint(50, 500),
                location=locations[i % len(locations)],
                host=host,
                max_guests=random.randint(1, 6),
                amenities=amenities[i % len(amenities)],
                images=[f'https://example.com/image{i}.jpg']
            )
            listings.append(listing)
            self.stdout.write(f'Created listing: {listing.title}')

        # Create sample bookings
        for i in range(15):
            listing = random.choice(listings)
            guest = random.choice([u for u in users if u != listing.host])
            check_in = datetime.now().date() + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 7))
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in=check_in,
                check_out=check_out,
                status=random.choice(['pending', 'confirmed', 'completed']),
                total_price=listing.price * (check_out - check_in).days,
                number_of_guests=random.randint(1, listing.max_guests)
            )
            self.stdout.write(f'Created booking: {booking}')

        # Create sample reviews
        for listing in listings:
            # Get all users except the host
            potential_reviewers = [u for u in users if u != listing.host]
            # Randomly select 1-3 unique reviewers
            num_reviews = min(random.randint(1, 3), len(potential_reviewers))
            reviewers = random.sample(potential_reviewers, num_reviews)
            
            for reviewer in reviewers:
                Review.objects.create(
                    listing=listing,
                    user=reviewer,
                    rating=random.randint(3, 5),
                    comment=f'Great place to stay! {random.choice(["Very clean", "Excellent location", "Amazing host"])}'
                )
            self.stdout.write(f'Created {num_reviews} reviews for listing: {listing.title}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database')) 