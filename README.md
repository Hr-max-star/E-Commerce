
E-Commerce Backend System (Django REST API)
1. Project Overview

This project is a backend system for an E-commerce application, built using Django and Django REST Framework.

It supports public product browsing, admin and customer authentication, guest checkout, and complete order–payment–invoice flow.
The project is designed to reflect real-world backend architecture, focusing on clean models, permissions, and scalable REST APIs.

2. What This Project Does

Browse products and categories without login

Admin login using email & password

Customer login using mobile number & OTP

Guest checkout support

Manage products, orders, payments, and invoices

Uses soft delete instead of permanent deletion

Follows REST API best practices

3. Technologies Used

Python

Django

Django REST Framework

PostgreSQL

Git & GitHub

4. Core Models
Model Name	Key Fields	Description
User	email, mobile_number, password, otp, role flags	Handles admin and customer authentication.
Store	name, owner, contact_email, contact_phone	Represents a seller or store.
Category	name, slug, description	Top-level product grouping.
Subcategory	name, category (FK)	Subdivision of a category.
Product	sku, name, price, inventory_count, category, store	Sellable item with inventory tracking.
ProductImage	product (FK), image, order	Stores multiple images per product.
Order	user, store, total_amount, status	Represents an order placed by guest or customer.
OrderItem	order (FK), product (FK), quantity, unit_price	Individual items inside an order.
Payment	order (FK), payment_method, transaction_id, status	Stores payment transaction details.
Invoice	order (FK), invoice_number, amount	Generated invoice for each order.
Relationship Summary

One User → Many Orders

One Store → Many Products

One Category → Many Subcategories

One Product → Many ProductImages

One Order → Many OrderItems

One Order → One Payment

One Order → One Invoice

5. Shared Base Model

All major models inherit from a common BaseModel to maintain consistency.

BaseModel Fields
Field Name	Purpose
status_flag	Status indicator (ACTIVE, INACTIVE, etc.)
comments	Additional notes
active_from / active_to	Validity period
cdate / mdate	Created and modified timestamps
cuser / muser	Created by / modified by
is_deleted	Soft delete flag
is_suspended	Suspension flag

This helps with auditing, lifecycle tracking, and safe deletion.

6. Authentication & Authorization
Authentication Types

Admin → Email + Password

Customer → Mobile Number + OTP

Guest → No login required

OTP is set to 1234 for development/testing.

Access Rules
Action	Access
View products & categories	Public
Manage products & categories	Admin / Store staff
Place order	Guest or Customer
View order details	Order owner or Admin
7. API Overview
Public APIs
GET /api/categories/
GET /api/products/
GET /api/products/{id}/

Authentication APIs
POST /api/auth/admin/login/
POST /api/auth/customer/login/
POST /api/auth/customer/request-otp/

Protected APIs
POST /api/products/
POST /api/orders/
GET  /api/orders/{id}/

8. Key Features

RESTful API design

Role-based access control

Guest checkout support

Soft delete for records

Scalable and extensible data models

Ready for payment gateway integration

9. Installation & Setup
git clone https://github.com/Hr-max-star/E-Commerce.git
cd Ecommerce_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

10. Notes & Future Improvements

Replace hardcoded OTP with real SMS service

Integrate payment gateway (Stripe / Razorpay)

Generate invoice PDFs

Add caching for performance optimization

11. Learning Outcomes

Django REST Framework architecture

Authentication and permission handling

Real-world database relationships

Clean backend project structure

Professional Git & GitHub workflow

12. Author

Hari
Backend Developer – Django & REST APIs
