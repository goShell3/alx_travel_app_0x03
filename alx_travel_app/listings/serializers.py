from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Payment


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing hosts model

    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing hosts model

    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing hosts model

    """
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'location',
            'host', 'is_available', 'max_guests', 'amenities',
            'images', 'created_at', 'updated_at', 'reviews',
            'average_rating'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

class BookingSerializer(serializers.ModelSerializer):

    """
    Serializer for booking 
    """
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        write_only=True,
        source='listing'
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in',
            'check_out', 'status', 'total_price', 'number_of_guests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['guest', 'status', 'total_price'] 

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
