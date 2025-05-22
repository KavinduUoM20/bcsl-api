# BCSL API Project Index

This document provides an index of all files in the BCSL API project with descriptions of their purpose.

## Project Overview

BCSL API is a FastAPI-based backend service that provides RESTful API endpoints for managing companies, members, and users. The project uses SQLModel (which combines SQLAlchemy and Pydantic) for database models and async PostgreSQL for data storage.

## Directory Structure

### Root Directory

- `.gitignore` - Git configuration file specifying which files to ignore in version control
- `requirements.txt` - Python dependencies for the project

### App Directory (`app/`)

#### Main Application Files

- `__init__.py` - Package initialization file
- `main.py` - Application entry point that configures FastAPI, sets up database initialization, and includes API routers

#### API Routes (`app/api/v1/routes/`)

- `__init__.py` - Package initialization file
- `company.py` - API endpoints for CRUD operations on companies
- `user.py` - API endpoints for user operations (currently simplified implementation)

#### Core Configuration (`app/core/`)

- `__init__.py` - Package initialization file
- `config.py` - Application configuration using Pydantic settings, loads environment variables from .env file

#### Database (`app/db/`)

- `__init__.py` - Package initialization file
- `init_db.py` - Database initialization logic, creates tables based on SQLModel metadata
- `session.py` - Database session configuration, sets up async SQLAlchemy engine and session factory

#### Models (`app/models/`)

- `__init__.py` - Package initialization file
- `company.py` - SQLModel for Company entity with PostgreSQL-specific column types
- `external_link.py` - SQLModel for ExternalLink entity, related to Member
- `follower.py` - SQLModel for Follower entity, represents follower relationships between Members
- `image.py` - SQLModel for Image entity, used for Member avatars and cover images
- `member.py` - SQLModel for Member entity with relationships to other entities
- `social_link.py` - SQLModel for SocialLink entity, related to Member
- `user.py` - Simple User model (not using SQLModel, likely for demonstration)

#### Schemas (`app/schemas/`)

- `__init__.py` - Package initialization file
- `company.py` - Pydantic schemas for Company entity (Create, Read, Update)
- `external_link.py` - Pydantic schemas for ExternalLink entity
- `follower.py` - Pydantic schemas for Follower entity
- `image.py` - Pydantic schemas for Image entity
- `member.py` - Pydantic schemas for Member entity
- `social_link.py` - Pydantic schemas for SocialLink entity
- `user.py` - Simple Pydantic schema for User entity

#### Services (`app/services/`)

- `__init__.py` - Package initialization file
- `company_service.py` - Business logic for Company entity CRUD operations
- `member_service.py` - Business logic for Member entity (file exists but appears to be empty)
- `user_service.py` - Simple business logic for User entity (in-memory implementation)

### Tests (`tests/`)

- `db_connection_test.py` - Test script for PostgreSQL database connection

## Database Schema

### Main Entities

1. **Company**

   - Fields: id, name, industry, website, email, phone, address, description, created_at, updated_at
   - Primary entity for company information

2. **Member**

   - Fields: id, name, slug, user_name, wallet_key, bio, following, followers, joined_at, created_at, updated_at
   - Relationships: avatar (Image), cover_image (Image), socials (SocialLink), links (ExternalLink), followers_list (Follower)
   - Represents a member/user profile

3. **Image**

   - Fields: id, thumbnail, original
   - Used for storing image references for member avatars and cover images

4. **SocialLink**

   - Fields: id, title, link, icon, member_id
   - Represents social media links for a member

5. **ExternalLink**

   - Fields: id, title, link, member_id
   - Represents external website links for a member

6. **Follower**
   - Fields: id, follower_id, followed_id
   - Represents follower relationships between members

## API Endpoints

### Companies

- `GET /api/v1/companies/` - List all companies
- `GET /api/v1/companies/{company_id}` - Get a specific company
- `POST /api/v1/companies/` - Create a new company
- `PUT /api/v1/companies/{company_id}` - Update a company
- `DELETE /api/v1/companies/{company_id}` - Delete a company

### Users

- `GET /api/v1/users/` - List all users (simplified implementation)
- `POST /api/v1/users/` - Create a new user (simplified implementation)

## Database Configuration

The project uses PostgreSQL hosted on Neon (a serverless Postgres provider) as indicated in the database connection test.

## Project Status

The project appears to be in development with:

- Company functionality fully implemented
- User functionality partially implemented (simplified)
- Member-related models defined but service implementation incomplete
- Other related entities (Image, SocialLink, ExternalLink, Follower) defined but without implemented services or routes
