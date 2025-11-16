# Nabha Health Connect - Rural Telemedicine Platform

A comprehensive Django REST Framework backend for enabling rural patients to access healthcare remotely, even with poor connectivity.

## Features

- **User Management**: Patient, Doctor, Pharmacy, and Admin roles
- **Authentication**: JWT-based authentication with OTP support for low-literacy users
- **Appointments**: Booking system with availability checking
- **Teleconsultations**: Video/audio/chat consultation support
- **Medicine Management**: Master data and pharmacy inventory tracking
- **AI Symptom Checker**: Lightweight symptom analysis with caching
- **Health Records**: Digital health records management
- **Notifications**: SMS/WhatsApp integration ready
- **Analytics**: Dashboard for health department insights
- **Offline Support**: Sync endpoints for low-bandwidth scenarios

## Prerequisites

- Python 3.12+
- PostgreSQL (optional, SQLite for development)
- Virtual environment

## Installation

1. **Clone the repository**
   ```bash
   cd /home/ritesh/projects/swasth-be
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (copy from .env.example and update values)
   ```bash
   # Create .env file with your configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # 2Factor.in SMS API (for OTP)
   FACTOR2_API_KEY=your-2factor-api-key
   
   # Groq LLM API (for AI Symptom Checker)
   GROQ_API_KEY=your-groq-api-key
   GROQ_MODEL=llama-3.3-70b-versatile  # Optional, defaults to llama-3.3-70b-versatile
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
swasth-be/
├── accounts/          # Authentication & User Management
├── patients/          # Patient profiles & Health Records
├── doctors/           # Doctor profiles & Schedules
├── pharmacies/        # Pharmacy management
├── appointments/      # Appointment booking & Prescriptions
├── medicines/         # Medicine master data & Inventory
├── ai_symptom_checker/# AI Symptom Analysis
├── notifications/     # Notification system
├── analytics/         # Analytics & Reporting
└── core/              # Project settings
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/` - Get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/otp/request/` - Request OTP
- `POST /api/auth/otp/login/` - Login with OTP
- `GET /api/auth/profile/` - Get user profile

### Patients
- `GET /api/patients/profiles/` - List patients
- `POST /api/patients/profiles/` - Create patient profile
- `GET /api/patients/health-records/` - List health records

### Doctors
- `GET /api/doctors/profiles/` - List doctors
- `GET /api/doctors/profiles/{id}/schedule/` - Get doctor schedule

### Appointments
- `GET /api/appointments/bookings/` - List appointments
- `POST /api/appointments/bookings/` - Book appointment
- `POST /api/appointments/bookings/check_availability/` - Check availability

### Medicines
- `GET /api/medicines/master/` - List medicines
- `GET /api/medicines/inventory/availability/` - Check medicine availability

### AI Symptom Checker
- `POST /api/ai-symptom-checker/check/` - Check symptoms
- `GET /api/ai-symptom-checker/history/` - Get check history

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/{id}/mark_read/` - Mark as read

### Analytics
- `GET /api/analytics/dashboard/` - Admin dashboard (admin only)

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## Configuration

### Database

For PostgreSQL, update your `.env` file:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=swasth_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### JWT Settings

Configure JWT token lifetimes in `.env`:
```
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)
```

## Testing

```bash
python manage.py test
```

## TODO

- [ ] Implement SMS/WhatsApp notification integration
- [ ] Add video consultation token generation
- [ ] Integrate actual AI model for symptom checking
- [ ] Implement offline sync endpoints
- [ ] Add compression for API responses
- [ ] Implement multilingual support (Punjabi, Hindi)
- [ ] Add comprehensive test coverage
- [ ] Setup CI/CD pipeline
- [ ] Deploy to cloud infrastructure

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

This project is part of the Nabha Health Connect initiative.

## Team

Rural Telemedicine Platform - Punjab Health Department

