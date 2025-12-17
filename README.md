E-Commerce Backend API (Django)

This project is a backend API for an e-commerce application, built using Django and Django REST Framework.
It handles product catalog, user authentication, orders, payments, and invoices, with a clean and extensible data model.

The focus of this project is backend structure, security, and real-world API behavior, not just CRUD.

What this project does

Allows users to browse products and categories without login

Supports admin login using email & password

Supports customer login using mobile number & OTP

Allows guest checkout (no account required)

Manages orders, payments, and invoices

Uses PostgreSQL as the database

Follows REST API best practices

Common Base Model

All major models inherit from a shared BaseModel.
This keeps the system consistent and avoids repeated fields.

The base model provides:

Status and comments

Active date range

Created / modified timestamps

Created by / modified by user

Soft delete (is_deleted)

Suspend flag (is_suspended)

This makes auditing and lifecycle management easy across the application.

Main Models
User

Admin users log in using email + password

Customers log in using mobile number + OTP

OTP is set to 1234 for development

Role flags control permissions (admin, staff, customer)

Store

Represents a seller or shop

Linked to a user (store owner)

Stores contact and address information

Category & Subcategory

Used to organize products

Categories can be global or store-specific

Subcategories belong to a category

Product

Identified using a unique SKU

Linked to category, subcategory, and store

Tracks price and inventory

Supports multiple images and variant attributes

Product Image

Multiple images per product

Supports ordering and alt text

Order & Order Items

Orders can be placed by guests or logged-in users

Each order contains multiple order items

Tracks quantity, price, and totals

Order status is managed centrally

Payment

Stores payment method and transaction details

Designed to work with payment gateways

Can store webhook or metadata information

Invoice

Generated per order

Stores invoice number, dates, and amount

Designed for PDF export in future

Authentication & Access Rules

No authentication required to view products or categories

Authentication required to create or manage data

Admin and staff users manage catalog

Customers can place and view their own orders

Guests can place orders without login

Permissions are handled using Django REST Framework permission classes and custom checks where required.

API Overview (Examples)

Public APIs:

GET /api/categories/
GET /api/products/
GET /api/products/{id}/


Authentication:

POST /api/auth/admin/login/
POST /api/auth/customer/login/
POST /api/auth/customer/request-otp/


Protected APIs:

POST /api/products/
POST /api/orders/
GET  /api/orders/{id}/

Tech Stack

Python

Django

Django REST Framework

PostgreSQL

Git & GitHub

Development Notes

Uses soft delete instead of hard delete

OTP is hardcoded for development only

.env is used for secrets and database config

Designed to be extended with:

Real OTP service

Payment gateway

Invoice PDF generation

Local Setup
git clone https://github.com/Hr-max-star/E-Commerce.git
cd Ecommerce_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

About This Project

This project was built to:

Practice real-world backend architecture

Understand authentication flows

Work with relational data models

Follow clean Django REST patterns

Author

Hari
Backend Developer (Django, REST APIs)# E-Commerce
