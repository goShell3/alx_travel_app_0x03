# ALX Travel App

A Django-based travel accommodation platform that allows users to list properties, make bookings, and leave reviews.

## Features

- Property listings with detailed information
- Booking management system
- User reviews and ratings
- RESTful API endpoints
- Sample data seeder

## Models

### Listing
- Title and description
- Price and location
- Host (User) relationship
- Availability status
- Maximum guests capacity
- Amenities and images
- Timestamps

### Booking
- Listing relationship
- Guest (User) relationship
- Check-in and check-out dates
- Booking status (pending, confirmed, cancelled, completed)
- Total price calculation
- Number of guests
- Timestamps

### Review
- Listing relationship
- User relationship
- Rating (1-5)
- Comment
- Timestamps
- Unique constraint per user per listing

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/alx_travel_app.git
cd alx_travel_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Seed the database with sample data:
```bash
python manage.py seed
```

## API Endpoints

The API provides the following endpoints:

- `/api/listings/` - List and create property listings
- `/api/listings/<id>/` - Retrieve, update, or delete a specific listing
- `/api/bookings/` - List and create bookings
- `/api/bookings/<id>/` - Retrieve, update, or delete a specific booking
- `/api/reviews/` - List and create reviews
- `/api/reviews/<id>/` - Retrieve, update, or delete a specific review

## Sample Data

The seeder creates:
- 5 sample users
- 10 sample listings across different locations
- 15 sample bookings
- 1-3 unique reviews per listing

## Technologies Used

- Django 4.2+
- Django REST Framework 3.14+
- SQLite (development database)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
 
 ## Background Tasks with Celery

This project uses Celery with RabbitMQ for asynchronous task processing.

### Setup Requirements

1. Install RabbitMQ:
   ```bash
   sudo apt-get install rabbitmq-server