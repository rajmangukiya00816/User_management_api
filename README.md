# User Management API

The User Management API is a FastAPI application that provides user registration, authentication, data retrieval, and account deletion using Firebase services. This API allows you to manage user accounts in your application.

## Table of Contents
- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

To run the User Management API, you need the following prerequisites:

- [Python](https://www.python.org/downloads/) (Python 3.7 or higher)
- [FastAPI](https://fastapi.tiangolo.com/) (installed via pip)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) (provided as `eeee_service_account_keys.json`)
- [Pyrebase](https://github.com/thisbejim/Pyrebase) (installed via pip)
- [uvicorn](https://www.uvicorn.org/) (installed via pip)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/user-management-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd user-management-api
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Firebase Admin SDK
   - Replace `eeee_service_account_keys.json` with your own Firebase Admin SDK service account credentials. You can obtain these credentials from the Firebase Console.

2. Firebase Web Configuration
   - Configure your Firebase project and replace `firebase_config.json` with your Firebase web configuration.

### Running the Application

To start the FastAPI application, use the following command:

```bash
uvicorn main:app --reload
```

Replace `main` with the name of your Python file containing the FastAPI application if it's different.

The API will be accessible at [http://localhost:8000](http://localhost:8000).

## Endpoints

The User Management API exposes the following endpoints:

- `POST /signup`: Register a new user account.
- `POST /login`: Log in and obtain an authentication token (JWT).
- `PUT /update`: Update user full name or email.
- `GET /display`: Display user data based on the provided token.
- `DELETE /delete`: Delete a user account.

## API Documentation

### User Registration (POST /signup)

Register a new user account.

#### Request

- **URL**: `/signup`
- **Method**: `POST`
- **Body**:
  - `email` (string): User's email address.
  - `password` (string): User's password.
  - `username` (string): User's username.
  - `full_name` (string): User's full name.

#### Response

- **Status Code**: 200 (OK)
- **Body**:
  - `message` (string): "Successfully created user {user_id}"

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "Error! Missing Email or Password"

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "Error Creating User"

### User Login (POST /login)

Log in and obtain an authentication token (JWT).

#### Request

- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  - `email` (string): User's email address.
  - `password` (string): User's password.

#### Response

- **Status Code**: 200 (OK)
- **Body**:
  - `token` (string): Authentication token (JWT)

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "There was an error logging in"

### Update User Information (PUT /update)

Update user full name or email.

#### Request

- **URL**: `/update`
- **Method**: `PUT`
- **Body**:
  - `token` (string): Authentication token (JWT).
  - `full_name` (string, optional): Updated full name.
  - `email` (string, optional): Updated email.

#### Response

- **Status Code**: 200 (OK)
- **Body**:
  - `message` (string): "Username updated successfully"
  - `update_name` (string): Updated full name (if provided).

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "Please provide one param to update data"

- **Status Code**: 401 (Unauthorized)
- **Body**:
  - `message` (string): "Invalid token"

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "Error updating username"

### Display User Data (GET /display)

Display user data based on the provided token.

#### Request

- **URL**: `/display`
- **Method**: `GET`
- **Headers**:
  - `token` (string): Authentication token (JWT).

#### Response

- **Status Code**: 200 (OK)
- **Body**:
  - `uid` (string): User's unique ID.
  - `email` (string): User's email address.
  - `full_name` (string): User's full name.
  - `created_at` (string): Date and time of account creation.

- **Status Code**: 500 (Internal Server Error)
- **Body**:
  - `message` (string): "Unable to fetch user data"

### Delete User Account (DELETE /delete)

Delete a user account.

#### Request

- **URL**: `/delete`
- **Method**: `DELETE`
- **Body**:
  - `email` (string): User's email address.
  - `password` (string): User's password.

#### Response

- **Status Code**: 200 (OK)
- **Body**:
  - `message` (string): "User deleted successfully"

- **Status Code**: 400 (Bad Request)
- **Body**:
  - `message` (string): "Error deleting user"

## Contributing

If you would like to contribute to this project or report issues, please follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
