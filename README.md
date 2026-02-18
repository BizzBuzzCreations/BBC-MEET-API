# BBC Meet - Meeting Management Platform API

A robust Django-based API for managing meetings, tracking attendance via OTP verification, and documenting events with photo evidence. Designed for admins to oversee meeting operations and for users to schedule and verify meetings securely.

## 🚀 Features

*   **User Authentication**: Secure JWT-based authentication (Login/Register).
*   **Meeting Management**:
    *   Create, Read, Update, and Delete (CRUD) meetings.
    *   Track meeting status (Scheduled, In Progress, Completed, Cancelled).
    *   Specify meeting type (In Person, Online) and duration.
*   **Secure Verification**:
    *   **OTP Verification**: Organizers can generate an OTP, which is emailed to them. Participants/Organizers provide this OTP to verify the meeting completion.
*   **Evidence Gathering**:
    *   **Photo Uploads**: Upload multiple photos as proof of the meeting.
    *   Photos are linked to specific meetings and users.
*   **Admin Dashboard**:
    *   Comprehensive admin interface to search, filter, and manage meetings and photos.

## 🛠️ Tech Stack

*   **Backend Framework**: Django 6.0.2
*   **API Framework**: Django REST Framework (DRF)
*   **Authentication**: SimpleJWT (JSON Web Tokens)
*   **Database**: SQLite (Default)
*   **Email**: SMTP (configured for Gmail in settings)

## ⚙️ Installation & Setup

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/BizzBuzzCreations/BBC-MEET-API.git
cd BBC-MEET
```

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/macOS
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt django-environ pillow
```

### 4. Environment Configuration

Create a `.env` file in the root directory (`c:\BBC-MEET\.env`) and add the following configurations:

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=*
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> **Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/`.

## 📖 API Endpoints

### Authentication (`/api/auth/`)

*   `POST /create/`: Register a new user.
*   `POST /login/`: Login and obtain JWT tokens (`access`, `refresh`).
*   `GET /profile/`: Get current user profile.

### Meetings (`/api/meet/`)

*   `GET /`: List all meetings.
*   `POST /`: Create a new meeting.
*   `GET /{uid}/`: Retrieve specific meeting details.
*   `PUT /{uid}/`: Update meeting details.
*   `DELETE /{uid}/`: Delete a meeting.

### Verification & Evidence

*   `POST /{uid}/generate-otp/`: Generate and email OTP to the organizer.
*   `POST /{uid}/verify-otp/`: Verify the meeting with the code.
    *   Body: `{"otp_code": "123456"}`
*   `POST /{uid}/upload-photo/`: Upload a photo proof.
    *   Body: `multipart/form-data`, Key: `file`

## 📸 Admin Panel

Access the comprehensive admin panel at:
`http://127.0.0.1:8000/admin/`

Here you can:
*   View all meetings and their current status.
*   See uploaded photos inline with meeting details.
*   Filter meetings by status, type, and date.
