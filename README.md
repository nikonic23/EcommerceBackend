🛒 E-COMMERCE BACKEND (Flask + MySQL)

A production-style e-commerce backend built using Flask, MySQL, and JWT-based authentication.
Designed with clean architecture, modular blueprints, service-layer separation, and full test coverage.



✨ Features
🔐 Authentication & Authorization

• JWT-based authentication (access tokens)
• Role-based access control (Admin / User)
• Secure password hashing using bcrypt
• Token injection via session for browser-based flows



🛍️ Product Management

• Admin-only product creation, update, soft delete
• Public product listing
• Stock validation at order time
• Service-layer SQL separation (services.py)



🛒 Cart System

• Persistent carts per user
• Quantity aggregation
• Stock checks before adding
• Automatic cart cleanup after order placement



📦 Orders & Checkout

• Atomic order placement
• Order-item relationship modeling
• Admin order management (status updates)
• Mock payment flow
• Stock rollback on cancellation



🧱 Architecture

Flask Application Factory pattern
• Modular Blueprints:
    • auth
    • main
    • products
    • cart
    • orders
    • admin
• Service layer for database logic
• Utility layers for helpers & decorators



🧪 Testing

• Pytest-based test suite
• Isolated test database
• Auth, cart, orders, products fully tested
• Fixtures via conftest.py



📊 Observability

• Structured logging
• Request ID propagation
• Log-level testing



🗂️ Project Structure

.
├── app.py
├── config.py
├── extensions.py
├── auth/
│   ├── routes.py
│   ├── forms.py
│   └── __init__.py
├── products/
│   ├── routes.py
│   ├── services.py
│   └── __init__.py
├── cart/
│   ├── routes.py
│   └── __init__.py
├── orders/
│   ├── routes.py
│   └── __init__.py
├── admin/
│   ├── routes.py
│   └── __init__.py
├── utils/
│   ├── helpers.py
│   ├── decorators.py
│   └── logging.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_cart.py
│   ├── test_orders.py
│   └── test_products.py
└── readme.txt



🛠️ Tech Stack

• Backend: Flask
• Database: MySQL
• Auth: Flask-JWT-Extended
• ORM: Raw SQL (intentional, explicit control)
• Testing: Pytest
• Security: bcrypt, JWT
<<<<<<< Updated upstream
• Logging: Python logging
=======
• Logging: Python logging
>>>>>>> Stashed changes
