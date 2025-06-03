
# 🏡 HBnB Project – Holberton School

Create comprehensive technical documentation that will serve as the foundation for the development of the HBnB Evolution application to understand the overall architecture, the detailed design of the business logic, and the interactions within the system.

---

## 📚 Table of Contents

* [Overview](#overview)
* [Architecture](#architecture)
* [Task 0: Presentation Layer (View)](#task-0-presentation-layer-view)
* [Task 1: Database Models & Relationships](#task-1-database-models--relationships)
* [Task 2: Sequence Diagrams](#task-2-sequence-diagrams)
* [Authors](#author)

---

## 📌 Overview

The HBnB project is a web platform for listing, discovering, and booking accommodations. It supports:

* User authentication
* Search and filtering
* Viewing and managing room listings
* Leaving reviews
* Hosting functionality

---

## 🏗️ Architecture

The app is divided into three layers:

### 🔹 Presentation Layer (Frontend)

* Search interface, room details, profile management
* Routes like `/rooms/:id`, `/signup_login`, `/become-a-host`

### 🔸 Business Logic Layer (Controllers/Services)

* Validates data
* Handles permissions, authentication, and validation
* Routes interact with models and services

### 🔻 Persistence Layer (Database)

* Relational tables (e.g., Place, User, Reservation, Review)
* Optionally uses NoSQL for storing JSON fields (like photos or user preferences)

---

## 🎯 Task 0: Presentation Layer (View)
![Concept map - Page 1](https://github.com/user-attachments/assets/bf9ea4c7-0ed7-496a-a882-927e66e5f1aa)

| Feature                  | Route                                                       |
| ------------------------ | ----------------------------------------------------------- |
| Search stays             | `/s/location-name`                                          |
| City & country stays     | `/{city}-{country}/stays`                                   |
| Filtered homes           | `/s/{city}--{state}/homes?option=value`                     |
| Sign Up / Login          | `/signup_login`                                             |
| Become a Host            | `/become-a-host`, `/hosting`                                |
| Add/Edit Listing         | `/hosting/listings/editor/<id>/details/photo-tour`          |
| View Room Details        | `/rooms/<id>`                                               |
| Room Reviews             | `/rooms/<id>/reviews`                                       |
| User Profile             | `/user/profile/about`, `/users/profile/about?editMode=true` |
| Past Trips & Connections | `/users/profile/past-trip`, `/user/profile/connection`      |

API Interactions:

* `GET /rooms`
* `POST /login`
* `POST /rooms/:id/review`
* `DELETE /rooms/:id`

---

## 🧱 Task 1: Database Models & Relationships

![Concept map - Page 2](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/Business%20Logic%20Layer.svg)
Entities:

### `User`

* Auth info, profile, and image
* Fields: `id`, `email`, `encreypted_password`, `phone_number`, `image_url`, etc.

### `Place`

* Core listing info
* Fields: `id`, `title`, `description`, `price`, `photo_url`, `owner_id`, `type_of_place`, etc.
* Linked to `User`, `Amentity`, and `Reservation`

### `Review`

* Fields: `id`, `user_id`, `place_id`, `rating`, `comment`, `time`

### `Amentity`

* Fields: `id`, `place_id`, `name`, `description`, `count`

### `Reservation`

* Fields: `id`, `user_id`, `place_id`, `start_date`, `end_date`, `price`, `discount`

### `User_Custom_Field`

* For extensible user data
* Fields: `key`, `label`, `type`, `isRequired`, `displayOrder`

---

## 🔁 Task 2: Sequence Diagrams

### 1. **Sign Up / Login**

![sequence](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/Sign%20up_%20Login.png)

### 2. **Get Room Details**
![sequence_room_details](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/squence_Get%20Room%20Details.svg)


### 3. **Add Review**

![sequence_add_review](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/squence_Add%20Review.svg)

### 4. **Delete Place**

![delete_place](https://github.com/marwa-mh/holbertonschool-hbnb/blob/main/squence_Delete%20Place.svg)

---

## 👩‍💻 Authors

* **Marwa Al Mahmoud**
* **Lily Duong**
* **Mat Dickson**


