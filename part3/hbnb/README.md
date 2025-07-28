# Holberton School HBnB - Part 3

This is the third part of the **HBnB** project from Holberton School, focused on building a RESTful API with Flask to manage users, places, reviews, and amenities. The backend is powered by SQLAlchemy ORM, and JWT authentication is implemented for secure access.

## ✨ Features

- JWT-based user authentication
- Role-based access (Admin vs Normal User)
- CRUD operations for:
  - Users
  - Places
  - Reviews
  - Amenities
- Many-to-many relationship between **Places** and **Amenities**
- Data validation and clean architecture with a service (facade) layer
- Swagger UI via Flask-RESTx for API documentation

## 🧱 Database Schema

The application uses MySql database via SQLAlchemy with clearly defined relationships:

- `User` has many `Place` and many `Review`
- `Place` has many `Review`
- `Place` has many `Amenity` via a junction table `place_amenity`

### 📊 Entity-Relationship Diagram

![DB Diagram](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/part3/hbnb/hbnb_p3_db.png)


