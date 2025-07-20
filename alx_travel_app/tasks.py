from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(recipient_email, booking_details):
    subject = 'Your Booking Confirmation'
    message = f'Thank you for your booking!\n\nDetails:\n{booking_details}'
    from_email = settings.EMAIL_HOST_USER
    
    send_mail(
        subject,
        message,
        from_email,
        [recipient_email],
        fail_silently=False,
    )
    return f"Email sent to {recipient_email}"