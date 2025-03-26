CREATE DATABASE Online_Taxi_Booking_System;
USE Online_Taxi_Booking_System;
SHOW TABLES;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each user
    user_type ENUM('Driver', 'Customer') NOT NULL, -- Type of user (Driver or Customer)
    full_name VARCHAR(100) NOT NULL, -- Full name of the user
    email VARCHAR(100) NOT NULL UNIQUE, -- Email address (unique)
    phone VARCHAR(15) NOT NULL, -- Phone number
    password VARCHAR(255) NOT NULL, -- Password (hashed for security)
    car_number VARCHAR(50), -- Car number (only for drivers)
    license_number VARCHAR(50) -- License number (only for drivers)
);

-- Remove username column if it exists
ALTER TABLE users DROP COLUMN username;

-- Show all users
SELECT * FROM users;

-- Create rides table
CREATE TABLE rides (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- Unique identifier for each ride
    
    current_location VARCHAR(255) NOT NULL,      -- Customer's current location
    target_location VARCHAR(255) NOT NULL,       -- Customer's destination location
    travel_date DATE NOT NULL,                   -- Travel date for the ride
    booking_time TIME NOT NULL,                  -- Booking time for the ride
    fare DECIMAL(10, 2),                         -- Fare for the ride (generated)
    booking_status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',  -- Ride status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the ride is booked
);

-- Show all rides
SELECT * FROM rides;

-- First, let's modify the column without the default value:
ALTER TABLE rides
MODIFY COLUMN booking_status ENUM('Scheduled', 'Completed', 'Cancelled');

-- Now set the default value separately:
ALTER TABLE rides
ALTER COLUMN booking_status SET DEFAULT 'Scheduled';

-- Verify the column modification
DESCRIBE rides;
use users;
ALTER TABLE rides DROP COLUMN user_id;