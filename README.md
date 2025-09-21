# CampusFlow API

A robust backend API for a College Management System, built with FastAPI and PostgreSQL. This API handles student, course, department, enrollment, and professor management, along with a secure authentication system.

## Live Deployed Application

*   **Base URL:** [https://campusflow-4n9z.onrender.com](https://campusflow-4n9z.onrender.com)
*   **API Documentation (Swagger UI):** [https://campusflow-4n9z.onrender.com/docs](https://campusflow-4n9z.onrender.com/docs)

## Features

*   **Authentication:** User registration, login (JWT token generation), role-based access control (Admin, Student, Professor).
*   **Students:** Create, read, update, and delete student records.
*   **Courses:** Create, read, update, and delete course information.
*   **Departments:** Manage academic departments.
*   **Enrollments:** Handle student enrollment in courses.
*   **Professors:** Manage professor records.

## Technologies Used

*   **FastAPI:** Modern, fast (high-performance) web framework for building APIs with Python 3.7+.
*   **PostgreSQL:** Powerful, open-source object-relational database system.
*   **Uvicorn:** ASGI server for running FastAPI applications.
*   **Pydantic:** Data validation and settings management using Python type hints.
*   **Passlib:** Secure password hashing library.
*   **Psycopg2:** PostgreSQL adapter for Python.
*   **python-jose:** JOSE (JSON Object Signing and Encryption) implementation for Python (used for JWT).

## Local Development Setup

Follow these steps to get your project running on your local machine.

### Prerequisites

*   Python 3.10+
*   PostgreSQL installed and running
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/darshilvasoya/CampusFlow_FastAPI_Project.git
cd CampusFlow_FastAPI_Project
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup (Local PostgreSQL)

Ensure your local PostgreSQL server is running.

*   **Create Database:** Create a new database named `student_database`.
    ```sql
    CREATE DATABASE student_database;
    ```
*   **Create Tables:** Connect to `student_database` using a tool like pgAdmin 4 or `psql` and run the following SQL commands to create the necessary tables:

    ```sql
    CREATE TABLE departments (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INTEGER NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE courses (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        code VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        credits INTEGER NOT NULL,
        department_id INTEGER REFERENCES departments(id)
    );

    CREATE TABLE enrollments (
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(id),
        course_id INTEGER REFERENCES courses(id),
        enrollment_date DATE,
        grade VARCHAR(2)
    );

    CREATE TABLE professors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        department_id INTEGER REFERENCES departments(id),
        title VARCHAR(255)
    );

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        email VARCHAR(255),
        full_name VARCHAR(255),
        disabled BOOLEAN,
        role VARCHAR(255),
        hashed_password VARCHAR(255) NOT NULL
    );
    ```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 6. Access API Documentation

Open your browser and go to `http://127.0.0.1:8000/docs` to view the interactive Swagger UI documentation.

## Deployment to Render

This project is configured for automatic deployment to Render using a `render.yaml` Blueprint.

1.  **Fork/Clone** this repository to your GitHub account.
2.  Go to your **Render Dashboard**.
3.  Click **New** and select **Blueprint**.
4.  Connect your GitHub account and select your `CampusFlow_FastAPI_Project` repository.
5.  Render will detect the `render.yaml` file. Give your service group a name (e.g., `campusflow`).
6.  Click **Apply**. Render will automatically provision a PostgreSQL database and deploy your FastAPI application.

### Post-Deployment Steps on Render

After your service is deployed on Render:

1.  **Create Tables on Render Database:** Your Render database will be empty. You need to connect to it using pgAdmin 4 (using the external connection details provided by Render) and run the `CREATE TABLE` SQL commands listed in the "Database Setup" section above.
2.  **Create Admin User:**
    *   Go to your deployed API's `/docs` page (e.g., `https://campusflow-4n9z.onrender.com/docs`).
    *   Use the `POST /register` endpoint to create a new user (e.g., username `Your_Registered_Username`, password `Your_Password`). This user will initially have the "student" role.
    *   Connect to your Render database via pgAdmin 4 and run the following SQL command to make this user an admin:
        ```sql
        UPDATE users SET role = 'admin' WHERE username = 'YOUR_REGISTERED_USERNAME';
        ```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

1.  **Register:** Use `POST /register` to create a new user.
2.  **Login:** Use `POST /token` with your username and password to obtain an `access_token`.
3.  **Authorize:** Include the `access_token` in the `Authorization` header of subsequent requests (e.g., `Bearer YOUR_ACCESS_TOKEN`). You can use the "Authorize" button in the Swagger UI (`/docs`) to do this easily.

## API Endpoints

*   `/`: Welcome message
*   `/token`: Authenticate and get an access token
*   `/register`: Register a new user
*   `/users/{username}/role`: Update a user's role (Admin only)
*   `/students`: Manage student records
*   `/courses`: Manage course information
*   `/departments`: Manage departments
*   `/enrollments`: Manage enrollments
*   `/professors`: Manage professor records

## Contact

For any inquiries, please contact: [workmail.darshaetherategmail.com](mailto:workmail.darshaetherategmail.com)
