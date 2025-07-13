from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

from .tasks import send_booking_confirmation_email

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        
        # Prepare booking details for email
        booking_details = f"""
        Property: {booking.property.title}
        Check-in: {booking.check_in}
        Check-out: {booking.check_out}
        Total Price: {booking.total_price}
        """
        
        # Trigger async email task
        send_booking_confirmation_email.delay(
            recipient_email=self.request.user.email,
            booking_details=booking_details
        )
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from decouple import config
import uuid, requests

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer

CHAPA_SECRET_KEY = config("CHAPA_SECRET_KEY")

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Initiate Chapa Payment
        tx_ref = str(uuid.uuid4())
        amount = booking.total_price  # assume your Booking model has this field
        email = booking.email         # assumes Booking model has email field
        name = booking.name           # or split into first_name, last_name

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "amount": str(amount),
            "currency": "ETB",
            "email": email,
            "first_name": name,
            "last_name": "",
            "tx_ref": tx_ref,
            "callback_url": "https://yourdomain.com/api/bookings/verify-payment/",
            "return_url": "https://yourdomain.com/payment-success/",
            "customization": {
                "title": "Booking Payment",
                "description": f"Payment for booking {booking.id}",
            }
        }

        response = requests.post("https://api.chapa.co/v1/transaction/initialize", headers=headers, json=data)
        res_data = response.json()

        if res_data["status"] == "success":
            Payment.objects.create(
                booking_reference=booking.id,
                amount=amount,
                chapa_tx_ref=tx_ref,
                status="Pending"
            )
        else:
            # Optionally: delete booking if payment fails
            booking.delete()
            raise Exception("Payment initialization failed")

    @action(detail=False, methods=['get'])
    def verify_payment(self, request):
        tx_ref = request.query_params.get('tx_ref')
        try:
            payment = Payment.objects.get(chapa_tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=404)

        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

        res = requests.get(url, headers=headers)
        data = res.json()

        if data['status'] == 'success':
            payment.status = 'Completed' if data['data']['status'] == 'success' else 'Failed'
            payment.chapa_order_id = data['data'].get('id')
            payment.save()
            return Response({'status': payment.status})
        return Response({'error': 'Verification failed'}, status=400)
