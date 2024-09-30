# User Service

This **User Service** is a standalone microservice for managing user authentication and account features. It includes
user registration, email verification, login, password management (forgot/reset), and profile handling. Built
with `FastAPI`, it utilizes `JWT` for secure authentication and supports both database interaction and email
notifications.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

---

## Features

- **User Registration**: Allows users to create a new account.
- **Email Verification**: Confirms the user's email address after registration.
- **Login**: Authenticates users and provides an access token.
- **Forgot Password**: Sends a password reset link to the user's email.
- **Reset Password**: Allows users to set a new password using the reset token.
- **User Profile**: Lets users view and update their profile.

---

## Requirements

- Python 3.12+
- FastAPI
- Pydantic 2.0+
- HTTPX
- Pytest
- SQLAlchemy (or another ORM for persistence)
- JWT (JSON Web Token for authentication)
- Email Server (SMTP or similar)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/e-wallet-user-service.git
   cd e-wallet-user-service

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file with the following variables:

   ```bash
      # Enable multi databases replication (true/false)
      USE_DB_REPLICATION=false
      
      # Default database (used if USE_DB_REPLICATION is false)
      DATABASE_URL=mysql+asyncmy://user:password@localhost/database_name
      
      # Master and slave databases (used if USE_DB_REPLICATION is true)
      DATABASE_WRITE_URL=mysql+asyncmy://user:password@localhost/database_name
      DATABASE_READ_URL=mysql+asyncmy://user:password@haproxy/database_name
      
      # JWT config
      SECRET_KEY=JWT_KEY_HERE
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      
      # Email settings
      SMTP_SERVER=smtp.gmail.com
      SMTP_PORT=587
      SMTP_USER=hello@gmail.com
      SMTP_PASSWORD=APPLICATION_PASSWORD
      SMTP_FROM_EMAIL=hello@gmail.com
      
  ```

      
---

## Usage

1. Run the FastAPI server locally:
   ```bash
   uvicorn app.main:app --reload

2. Access the API documentation at `http://127.0.0.1:8000/docs`.
3. Example registration request:
   ```bash
   curl -X POST "http://127.0.0.1:8000/users/register" \
   -H "Content-Type: application/json" \
   -d '{"first_name": "john", "last_name": "deo", "email": "john.doe@example.com", "password": "StrongPassword123!"}'

---

## API Endpoints

### 1. User Registration

- **Endpoint**: `/users/register`
- **Method**: `POST`
- **Description**: Registers a new user in the system.
- **Request Body**:
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "password": "strong_password"
    }
    ```
- **Response**:
    - `201 Created`: User registered successfully.
    - `422 Validation Error`: Validation error or user already exists.

### 2. Email Verification

- **Endpoint**: `/users/confirm-email`
- **Method**: `POST`
- **Description**: Verifies the user's email after registration.
- **Request Body**:
    ```json
    {
      "email": "john.doe@example.com",
      "code": "email_verification_code"
    }
    ```
- **Response**:
    - `200 OK`: Email verified successfully.
    - `422 Validation Error`: Invalid email or code.

### 3. Login

- **Endpoint**: `/users/login`
- **Method**: `POST`
- **Description**: Authenticates the user and returns an access token.
- **Request Body**:
    ```json
    {
      "email": "john.doe@example.com",
      "password": "strong_password"
    }
    ```
- **Response**:
    - `200 OK`: Login successful, returns a JWT token.
    - `422 Validation Error`: Invalid credentials.

### 4. Forgot Password

- **Endpoint**: `/users/forgot-password`
- **Method**: `POST`
- **Description**: Sends a password reset link to the user's email.
- **Request Body**:
    ```json
    {
      "email": "john.doe@example.com"
    }
    ```
- **Response**:
    - `200 OK`: Password reset link sent.
    - `422 Validation Error`: User with that email does not exist.

### 5. Reset Password

- **Endpoint**: `/users/reset-password/{code}`
- **Method**: `POST`
- **Description**: Allows users to reset their password using a valid reset code.
- **Request Body**:
    ```json
    {
      "new_password": "new_strong_password"
    }
    ```
- **Response**:
    - `200 OK`: Password reset successfully.
    - `422 Validation Error`: Invalid or expired reset token.

### 6. User Profile

- **Endpoint**: `/users/profile`
- **Method**: `GET`
- **Description**: Fetches the authenticated user's profile.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    - `200 OK`: Returns user profile.
    - `401 Unauthorized`: Invalid or missing token.

---

## Testing

The project includes unit and integration tests for the core functionalities. To run the tests, follow these steps:

1. Run tests using pytest:
    ````bash
    pytest

---

## License

- This project is licensed under the MIT License.

---

## Contact

If you have any questions, issues, or suggestions regarding this project, feel free to reach out:

- **Email**: [me@mahmoud-mohsen.com](mailto:me@mahmoud-mohsen.com)

I am happy to assist and answer any queries related to this service.
