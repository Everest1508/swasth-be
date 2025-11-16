# Web Portal Guide - Nabha Health Connect

## Overview

A complete web portal for doctors and pharmacists to apply and join the platform, with admin approval workflow and email notifications.

## Features Implemented

### 1. Application System
- **Doctor Applications**: Doctors can apply with professional details, qualifications, and documents
- **Pharmacy Applications**: Pharmacies can apply with business details and license information
- **Status Tracking**: Applications have pending/approved/rejected status

### 2. Admin Approval Workflow
- Admin can view all pending applications
- Admin can approve or reject applications
- Upon approval:
  - User account is automatically created
  - Doctor/Pharmacy profile is created
  - Email notification is sent with login credentials

### 3. Email Service (SMTP)
- Custom SMTP configuration model (not Django default)
- Admin can configure SMTP settings via Django admin
- Email notifications sent when:
  - Application is approved (with login credentials)
  - Application is rejected (with reason)

### 4. Web Portal Pages

#### Public Pages
- **Home Page** (`/`): Landing page with features and application links
- **Login Page** (`/login/`): Sectioned UI with branding on left, form on right
- **Apply as Doctor** (`/apply/doctor/`): Application form for doctors
- **Apply as Pharmacy** (`/apply/pharmacy/`): Application form for pharmacies

#### Authenticated Dashboards
- **Admin Dashboard** (`/dashboard/`): View and manage applications, SMTP settings
- **Doctor Dashboard** (`/dashboard/`): Manage schedule, view appointments
- **Pharmacy Dashboard** (`/dashboard/`): Manage inventory, add stock

### 5. UI Design
- **Tailwind CSS**: Modern, responsive design
- **TailAdmin Style**: Clean, professional interface
- **Sectioned Login**: Split-screen design with branding
- **Modern Components**: Cards, forms, buttons with hover effects

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Configure SMTP (via Django Admin)
1. Go to `/admin/`
2. Navigate to "SMTP Configurations"
3. Add new SMTP configuration:
   - Name: e.g., "Gmail SMTP"
   - Host: smtp.gmail.com
   - Port: 587
   - Use TLS: Yes
   - Username: your-email@gmail.com
   - Password: your-app-password
   - From Email: your-email@gmail.com
   - From Name: Nabha Health Connect
   - Is Active: Yes

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Access the Portal
- Home: http://localhost:8000/
- Login: http://localhost:8000/login/
- Admin: http://localhost:8000/admin/

## API Endpoints

### Applications
- `POST /api/applications/doctors/` - Submit doctor application
- `POST /api/applications/pharmacies/` - Submit pharmacy application
- `GET /api/applications/doctors/` - List doctor applications (admin)
- `GET /api/applications/pharmacies/` - List pharmacy applications (admin)
- `POST /api/applications/doctors/{id}/approve/` - Approve/reject doctor application (admin)
- `POST /api/applications/pharmacies/{id}/approve/` - Approve/reject pharmacy application (admin)

## Workflow

### For Doctors/Pharmacists
1. Visit home page
2. Click "Apply as Doctor" or "Apply as Pharmacy"
3. Fill out application form
4. Submit application
5. Wait for admin review
6. Receive email notification when approved/rejected
7. Login with provided credentials
8. Access dashboard to manage schedule/inventory

### For Admin
1. Login to admin dashboard
2. View pending applications
3. Review application details
4. Approve or reject application
5. System automatically:
   - Creates user account
   - Creates doctor/pharmacy profile
   - Sends email notification

## File Structure

```
templates/
├── base.html              # Base template with Tailwind CSS
├── home.html              # Landing page
├── login.html             # Sectioned login page
├── apply_doctor.html      # Doctor application form
├── apply_pharmacy.html   # Pharmacy application form
├── admin_dashboard.html   # Admin dashboard
├── doctor_dashboard.html  # Doctor dashboard
└── pharmacy_dashboard.html # Pharmacy dashboard

applications/
├── models.py              # DoctorApplication, PharmacyApplication
├── views.py               # Application ViewSets
├── serializers.py         # Application serializers
└── urls.py                # Application URLs

email_service/
├── models.py              # SMTPConfiguration
├── service.py             # EmailService class
└── admin.py               # SMTP admin interface
```

## Notes

- CSRF protection is handled automatically by Django for form submissions
- File uploads are supported for documents
- Email service uses custom SMTP configuration (not Django default)
- All dashboards are role-based and show relevant information
- UI follows TailAdmin design principles with Tailwind CSS

