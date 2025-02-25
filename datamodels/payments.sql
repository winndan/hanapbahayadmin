CREATE TABLE payments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE, -- Foreign key to bookings table
    payment_amount NUMERIC(10,2) NOT NULL CHECK (payment_amount > 0),
    payment_method TEXT NOT NULL CHECK (payment_method IN ('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer')),
    payment_status TEXT NOT NULL CHECK (payment_status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
    transaction_id TEXT NULL, -- Stores the transaction ID from the payment gateway
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);