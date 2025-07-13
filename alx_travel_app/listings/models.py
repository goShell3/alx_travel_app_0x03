from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    max_guests = models.PositiveIntegerField(default=1)
    amenities = models.JSONField(default=list)
    images = models.JSONField(default=list)

    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_guests = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.guest.username}'s booking at {self.listing.title}"

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('listing', 'user')

    def __str__(self):
        return f"{self.user.username}'s review for {self.listing.title}"

class Payment(models.Model):
    booking_reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Completed, Failed
    chapa_tx_ref = models.CharField(max_length=100, unique=True)
    chapa_order_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.status}"