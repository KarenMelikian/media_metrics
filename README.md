ERPNext Backend – Python Developer Assessment

This project is a FastAPI-based backend system built for a developer assessment. It features user registration, login with JWT authentication, dynamic form input storage, and CSV/Excel data import/export. The backend uses MariaDB for persistent storage and SQLAlchemy as the ORM.

🚀 Features

User Registration & Authentication (JWT-based)

Dynamic Input Fields (Add, Edit, Delete)

CSV and Excel Import/Export

MariaDB with SQLAlchemy & Alembic

Docker Compose support

📂 Tech Stack

Python 3.8+

FastAPI

SQLAlchemy 1.4+

Alembic

bcrypt (password hashing)

PyJWT (token authentication)

openpyxl (Excel handling)

MariaDB (database)

Docker & Docker Compose

💡 Setup Instructions

✅ 1. Clone the Repository

`git clone https://github.com/KarenMelikian/media_metrics.git`

`cd media_metrics`

✅ 2. Set Up Environment Variables

Create a .env file in the root directory:

`DB_HOST=localhost`

`DB_PORT=3306`

`DB_USER=''`

`DB_PASS=''`

`DB_NAME=''`

`JWT_SECRET=CTtub0jezl1M3U23O5of8vr-aw68O3mRI39YQdn_koHba5KyXIFwLQHfWP5OceoBs8ACNHT1Ip5HhfPR85xMXQ`

⚠️ Make sure DATABASE_URL matches Docker Compose credentials.

✅ 3. Docker Compose Setup (MariaDB)

✅ Run MariaDB via Docker Compose:

`docker-compose up -d`

MariaDB is now accessible at localhost:3306.

✅ 4. Create & Activate Virtual Environment

`python -m venv .venv`

`source .venv/bin/activate`  # Windows: `.venv\Scripts\activate`

✅ 5. Install Requirements

`pip install -r requirements.txt`

✅ 6. Alembic Migrations to DataBase

`alembic upgrade head`

✅ 7. Run the App

`python app/main.py`

📃 API Endpoints

Auth

POST /api/register: User registration

POST /api/login: Login and get JWT

Dynamic Fields

GET /api/dashboard/read: List all dynamic fields

POST /api/dashboard/create: Add new field

PUT /api/dashboard/update/{id}: Update field

DELETE /api/dashboard/delete/{id}: Delete field

Import/Export

GET /api/csv/export: Export fields as CSV

POST /api/csv/import: Import fields from CSV

GET /api/excel/export-excel: Export fields as Excel

POST /api/excel/import-excel: Import fields from Excel

🚫 Important Notes

Passwords are stored using bcrypt.

JWT tokens must be included in the Authorization header as Bearer <token>.

CORS and security best practices are applied.
