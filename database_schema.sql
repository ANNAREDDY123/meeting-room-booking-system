CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE employees(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100),
    role VARCHAR(50)
);

CREATE TABLE rooms(
    id INTEGER PRIMARY KEY,
    room_name VARCHAR(100),
    capacity INTEGER,
    location VARCHAR(100),
    is_available BOOLEAN
);

CREATE TABLE bookings(
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    room_id INTEGER,
    meeting_title VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME
);

CREATE TABLE participants(
    id INTEGER PRIMARY KEY,
    booking_id INTEGER,
    employee_name VARCHAR(100)
);
