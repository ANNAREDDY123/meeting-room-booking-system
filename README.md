# meeting-room-booking-system
FastAPI Meeting Room Booking System with Employee Management, Room Booking, Meeting Participants, JWT Authentication, SQLAlchemy ORM, Pagination, Background Tasks, and Docker Support.

## Features

- JWT Authentication
- Employee Management
- Room Management
- Room Booking
- Participants Management
- Pagination
- Background Tasks
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## APIs

### Authentication
POST /auth/register
POST /auth/login

### Employees
POST /employees
GET /employees
GET /employees/{id}
PUT /employees/{id}

### Rooms
POST /rooms
GET /rooms
GET /rooms/{id}
PUT /rooms/{id}

### Bookings
POST /bookings
GET /bookings
GET /bookings/{id}
DELETE /bookings/{id}

### Participants
POST /bookings/{booking_id}/participants
GET /bookings/{booking_id}/participants
