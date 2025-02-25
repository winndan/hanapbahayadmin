CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE rooms (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    room_number TEXT NOT NULL UNIQUE CHECK (char_length(room_number) BETWEEN 1 AND 50),
    room_type TEXT NOT NULL CHECK (room_type IN ('Standard', 'Family', 'Deluxe')),
    description TEXT NOT NULL,
    max_guests INT NOT NULL CHECK (max_guests > 0),
    status TEXT NOT NULL CHECK (status IN ('Available', 'Occupied', 'Under Maintenance')),
    price_per_night NUMERIC(10,2) NOT NULL CHECK (price_per_night > 0),
    image_id TEXT NULL, -- Stores image path in the Supabase storage bucket
    created_at TIMESTAMP DEFAULT NOW()
);
