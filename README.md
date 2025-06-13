# Weekly Scheduler API

A Django REST API for managing weekly schedules with time slots and associated IDs.

## Features

- CRUD operations for time slots and schedules
- JWT authentication
- Swagger/OpenAPI documentation
- Time slot validation
- Weekly schedule grouping by day

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /api/time-slots/` - List all time slots
- `POST /api/time-slots/` - Create a new time slot
- `GET /api/schedules/` - List all schedules
- `POST /api/schedules/` - Create a new schedule
- `GET /api/schedules/get-weekly-schedule/` - Get complete weekly schedule
- `GET /swagger/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation

## JWT Authentication

1. Obtain a JWT token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Use the token in subsequent requests:
```bash
Authorization: Bearer <your_token>
```

## Example Usage

Create a new time slot:
```bash
POST /api/time-slots/
{
    "day": "monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00"
}
```

Create a schedule:
```bash
POST /api/schedules/
{
    "time_slot": 1,
    "ids": [1, 2, 3]
}
```

## Project Structure

```
weekly_scheduler/
├── manage.py
├── requirements.txt
├── weekly_scheduler/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── schedule/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    └── views.py
```
