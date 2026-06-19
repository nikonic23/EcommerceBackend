# 🛒 E-Commerce Backend System

A production-style e-commerce backend built using Flask, MySQL, and JWT-based authentication. The project follows clean architecture principles with modular blueprints, service-layer separation, role-based authorization, and automated testing.

---

## Features

### 🔐 Authentication & Authorization

* JWT-based authentication using Flask-JWT-Extended
* Role-based access control (Admin / User)
* Secure password hashing with bcrypt
* Protected routes using custom decorators
* Token-based session handling

### 🛍️ Product Management

* Admin-only product creation, updates, and soft deletion
* Public product catalog APIs
* Inventory validation before order placement
* Service-layer abstraction for business logic

### 🛒 Cart System

* Persistent user-specific shopping carts
* Quantity aggregation for existing items
* Stock validation before cart updates
* Automatic cart cleanup after successful checkout

### 📦 Orders & Checkout

* Atomic order placement workflow
* Order and OrderItem relationship modeling
* Order status management for administrators
* Mock payment processing flow
* Stock restoration on order cancellation

---

## Architecture

### Design Principles

* Flask Application Factory Pattern
* Modular Blueprint Architecture
* Service Layer Separation
* Role-Based Access Control
* Centralized Utility Layer
* Test-Driven Development

### Modules

* Auth
* Products
* Cart
* Orders
* Admin
* Utilities

---

## Tech Stack

| Category        | Technology         |
| --------------- | ------------------ |
| Backend         | Flask              |
| Database        | MySQL              |
| Authentication  | Flask-JWT-Extended |
| Security        | bcrypt, JWT        |
| Testing         | Pytest             |
| Data Access     | Raw SQL            |
| Version Control | Git, GitHub        |

---

## Testing

The project includes a Pytest-based test suite covering:

* Authentication workflows
* Product management
* Cart functionality
* Order processing
* Authorization rules

Features include:

* Isolated test database
* Reusable fixtures via `conftest.py`
* Automated validation of business logic

---

## Project Structure

```text
.
├── app.py
├── config.py
├── extensions.py
├── auth/
├── products/
├── cart/
├── orders/
├── admin/
├── utils/
├── tests/
└── README.md
```

---

## Technical Highlights

* Implemented JWT-based authentication and authorization workflows
* Built role-based access control for secure admin operations
* Designed atomic checkout processes with inventory validation
* Structured application using modular blueprints and service layers
* Developed comprehensive automated tests using Pytest
* Implemented structured logging and request tracking mechanisms

---

## Future Improvements

* Payment Gateway Integration
* API Documentation (Swagger/OpenAPI)
* Docker Support
* Redis-Based Caching
* Background Job Processing
* CI/CD Pipeline

---

## Author

Nikhil Munda

GitHub: https://github.com/nikonic23