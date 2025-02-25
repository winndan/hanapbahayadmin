CREATE TABLE bookings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE, -- Foreign key to rooms table
    guest_name TEXT NOT NULL CHECK (char_length(guest_name) BETWEEN 1 AND 100),
    guest_email TEXT NOT NULL CHECK (guest_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'), -- Basic email validation
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INT NOT NULL CHECK (number_of_guests > 0),
    total_price NUMERIC(10,2) NOT NULL CHECK (total_price > 0),
    status TEXT NOT NULL CHECK (status IN ('Pending', 'Confirmed', 'Cancelled', 'Completed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Ensure check_out_date is after check_in_date
    CONSTRAINT valid_booking_dates CHECK (check_out_date > check_in_date)
);