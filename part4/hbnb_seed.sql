USE hbnb_p3_db;
-- Add users
INSERT INTO users(id, email, first_name, last_name, password, is_admin) VALUES
(UUID(), 'alice@example.com', 'Alice', 'Smith', '$2b$12$aIvq8K85HeJ4u/HvXe5K7eTNfR6FLtsLQZmIk.uz4BEs0SWKtOkbe', FALSE),
(UUID(), 'bob@example.com', 'Bob', 'Johnson', '$2b$12$aIvq8K85HeJ4u/HvXe5K7eTNfR6FLtsLQZmIk.uz4BEs0SWKtOkbe', FALSE),
(UUID(), 'charlie@example.com', 'Charlie', 'Brown', '$2b$12$aIvq8K85HeJ4u/HvXe5K7eTNfR6FLtsLQZmIk.uz4BEs0SWKtOkbe', FALSE),
(UUID(), 'diana@example.com', 'Diana', 'Lee', '$2b$12$aIvq8K85HeJ4u/HvXe5K7eTNfR6FLtsLQZmIk.uz4BEs0SWKtOkbe', FALSE),
(UUID(), 'ethan@example.com', 'Ethan', 'Williams', '$2b$12$aIvq8K85HeJ4u/HvXe5K7eTNfR6FLtsLQZmIk.uz4BEs0SWKtOkbe', FALSE);

-- Add amenities
INSERT INTO amenities(id, name) VALUES
(UUID(), 'WiFi'),
(UUID(), 'Swimming Pool'),
(UUID(), 'Air Conditioning'),
(UUID(), 'Parking'),
(UUID(), 'Pet Friendly'),
(UUID(), 'Kitchen'),
(UUID(), 'Washer'),
(UUID(), 'TV'),
(UUID(), 'Balcony'),
(UUID(), 'Fireplace');

-- Add places
INSERT INTO places(id, title, description, price, latitude, longitude, owner_id) VALUES
(UUID(), 'Cozy Apartment in Melbourne CBD',
 'Modern 1-bedroom apartment with stunning city views, close to Federation Square and public transport.',
 150.00, -37.8136, 144.9631,
 (SELECT id FROM users WHERE email = 'alice@example.com')),

(UUID(), 'Beach House in Bondi',
 'Relax in this 3-bedroom beach house just 5 minutes walk from Bondi Beach. Perfect for families and surfers!',
 320.00, -33.8908, 151.2743,
 (SELECT id FROM users WHERE email = 'bob@example.com')),

(UUID(), 'Mountain Cabin Retreat',
 'Rustic wooden cabin surrounded by nature, with fireplace and hiking trails nearby.',
 200.00, -37.3990, 145.8910,
 (SELECT id FROM users WHERE email = 'charlie@example.com')),

(UUID(), 'Luxury Penthouse in Sydney',
 'High-end 2-bedroom penthouse with panoramic harbour views, rooftop pool and gym access.',
 500.00, -33.8688, 151.2093,
 (SELECT id FROM users WHERE email = 'diana@example.com')),

(UUID(), 'Farm Stay in Hunter Valley',
 'Charming countryside farmhouse surrounded by vineyards, perfect for wine lovers.',
 180.00, -32.7758, 151.2992,
 (SELECT id FROM users WHERE email = 'ethan@example.com')),

(UUID(), 'Tropical Villa in Cairns',
 'Private villa with swimming pool, lush gardens, and Great Barrier Reef tours nearby.',
 350.00, -16.9186, 145.7781,
 (SELECT id FROM users WHERE email = 'alice@example.com')),

(UUID(), 'Stylish Loft in Brisbane',
 'Trendy loft apartment with open-plan living, close to cafes and nightlife.',
 220.00, -27.4698, 153.0251,
 (SELECT id FROM users WHERE email = 'bob@example.com')),

(UUID(), 'Eco Cottage in Tasmania',
 'Sustainable eco-friendly cottage with solar power, rainwater collection, and bushwalks at your doorstep.',
 140.00, -42.8821, 147.3272,
 (SELECT id FROM users WHERE email = 'charlie@example.com')),

(UUID(), 'Surf Shack in Byron Bay',
 'Laid-back surf shack just minutes from the beach, ideal for backpackers and surfers.',
 120.00, -28.6474, 153.6020,
 (SELECT id FROM users WHERE email = 'diana@example.com')),

(UUID(), 'Desert Glamping in Uluru',
 'Luxury tent glamping experience with breathtaking desert views of Uluru.',
 280.00, -25.3444, 131.0369,
 (SELECT id FROM users WHERE email = 'ethan@example.com'));

-- Map amenities (unchanged from your script)
-- ...

-- Add reviews
INSERT INTO reviews(id, text, rating, user_id, place_id) VALUES
(UUID(), 'Amazing location, super clean and comfortable!', 5,
 (SELECT id FROM users WHERE email = 'bob@example.com'),
 (SELECT id FROM places WHERE title = 'Cozy Apartment in Melbourne CBD')),

(UUID(), 'Perfect for a family holiday. The kids loved the pool!', 4,
 (SELECT id FROM users WHERE email = 'charlie@example.com'),
 (SELECT id FROM places WHERE title = 'Beach House in Bondi')),

(UUID(), 'Peaceful and relaxing, but a bit far from shops.', 3,
 (SELECT id FROM users WHERE email = 'alice@example.com'),
 (SELECT id FROM places WHERE title = 'Mountain Cabin Retreat')),

(UUID(), 'Absolutely stunning penthouse, worth every dollar!', 5,
 (SELECT id FROM users WHERE email = 'ethan@example.com'),
 (SELECT id FROM places WHERE title = 'Luxury Penthouse in Sydney')),

(UUID(), 'Great wine country escape, hosts were very welcoming.', 4,
 (SELECT id FROM users WHERE email = 'diana@example.com'),
 (SELECT id FROM places WHERE title = 'Farm Stay in Hunter Valley')),

(UUID(), 'Loved the tropical vibe, pool was amazing!', 5,
 (SELECT id FROM users WHERE email = 'charlie@example.com'),
 (SELECT id FROM places WHERE title = 'Tropical Villa in Cairns')),

(UUID(), 'Trendy place with great coffee shops nearby.', 4,
 (SELECT id FROM users WHERE email = 'alice@example.com'),
 (SELECT id FROM places WHERE title = 'Stylish Loft in Brisbane')),

(UUID(), 'Loved the eco-friendly design, very cozy.', 5,
 (SELECT id FROM users WHERE email = 'bob@example.com'),
 (SELECT id FROM places WHERE title = 'Eco Cottage in Tasmania')),

(UUID(), 'Fun and chilled vibe, perfect for a surf weekend.', 4,
 (SELECT id FROM users WHERE email = 'ethan@example.com'),
 (SELECT id FROM places WHERE title = 'Surf Shack in Byron Bay')),

(UUID(), 'Unforgettable experience, watching stars in the desert.', 5,
 (SELECT id FROM users WHERE email = 'alice@example.com'),
 (SELECT id FROM places WHERE title = 'Desert Glamping in Uluru'));