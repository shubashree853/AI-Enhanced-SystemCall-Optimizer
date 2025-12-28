# Django System Call Optimizer

A Django-based system call monitoring and optimization tool with user authentication, QR code login, and AI-powered recommendations.

## Features

- **User Management**: Three user roles (Admin, Staff, User) with different access levels
- **QR Code Authentication**: Unique QR codes for each user with revocation support
- **Registration & Login**: Traditional username/password and QR code-based login
- **System Call Optimizer**: Real-time monitoring and AI-powered optimization recommendations
- **Django Admin Panel**: Full admin interface for managing users, QR codes, and system data

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root (optional for Groq AI features):

```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_django_secret_key_here
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

When creating the superuser, you can set the role to 'admin' in the Django admin panel after creation.

### 5. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## User Roles

### Admin
- Full access to Django admin panel
- Can manage all users and QR codes
- Access to system call optimizer
- Can revoke/activate any QR code

### Staff
- Access to Django admin panel (limited)
- Can view users and QR codes
- Access to system call optimizer
- Can manage their own QR code

### User
- Access to dashboard
- Can generate/revoke their own QR code
- Access to system call optimizer (view only)

## Usage

### Registration

1. Navigate to `/register/`
2. Fill in the registration form
3. A QR code will be automatically generated for your account

### Login

**Traditional Login:**
1. Navigate to `/login/`
2. Enter username and password

**QR Code Login:**
1. Navigate to `/qr-login/`
2. Enter your QR code token or scan your QR code
3. You'll be automatically logged in

### Dashboard

After logging in, you can:
- View your user information
- View/download your QR code
- Revoke or regenerate your QR code
- Access the system call optimizer

### System Call Optimizer

Navigate to `/optimizer/` to:
- View real-time system call performance metrics
- See AI-powered optimization recommendations
- Filter and search system calls
- View detailed performance data

### Django Admin Panel

Access at `/admin/` to:
- Manage users and their roles
- View and manage QR codes
- Revoke/activate QR codes
- Regenerate QR codes
- View all system data

## QR Code Features

- **Unique QR Code**: Each user gets a unique QR code upon registration
- **Revocation**: Users can revoke their QR code for security
- **Regeneration**: Users can regenerate a new QR code at any time
- **Token-based Login**: QR codes contain unique tokens for authentication
- **Admin Management**: Admins can manage all QR codes from the admin panel

## API Endpoints

- `GET /optimizer/performance/` - Get performance data (requires login)
- `GET /optimizer/recommendations/` - Get optimization recommendations (requires login)
- `GET /optimizer/categories/` - Get syscall categories (requires login)
- `GET /optimizer/syscall/<name>/` - Get specific syscall details (requires login)
- `POST /api/qr-login/` - Login using QR code token (JSON: `{"token": "..."}`)

## Project Structure

```
syscall_optimizer/
├── manage.py
├── requirements.txt
├── syscall_optimizer/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                       # User management app
│   ├── models.py               # CustomUser and QRCode models
│   ├── views.py                # Authentication views
│   ├── admin.py                # Admin configuration
│   └── urls.py
├── optimizer/                  # System call optimizer app
│   ├── optimizer.py           # Core optimizer logic
│   ├── views.py                # Optimizer views
│   └── urls.py
└── templates/                  # HTML templates
    ├── base.html
    ├── users/
    └── optimizer/
```

## Notes

- The system call optimizer uses simulated data for demonstration purposes
- For production use on Linux, you can integrate eBPF monitoring
- QR code images are stored in `media/qr_codes/`
- Make sure to set `DEBUG=False` and configure proper `SECRET_KEY` for production

## Troubleshooting

**Issue: QR code not generating**
- Make sure `Pillow` is installed: `pip install Pillow`
- Check that `media/qr_codes/` directory exists and is writable

**Issue: Admin panel not accessible**
- Make sure you created a superuser: `python manage.py createsuperuser`
- Check that the user has `is_staff=True` or `role='admin'`

**Issue: Static files not loading**
- Run: `python manage.py collectstatic`
- Make sure `STATIC_URL` and `STATIC_ROOT` are configured correctly

## License

This project is licensed under the MIT License.
