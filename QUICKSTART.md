# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

## Step 4: Run the Server

```bash
python manage.py runserver
```

## Step 5: Access the Application

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Register**: http://127.0.0.1:8000/register/
- **Login**: http://127.0.0.1:8000/login/
- **QR Login**: http://127.0.0.1:8000/qr-login/
- **Optimizer**: http://127.0.0.1:8000/optimizer/

## User Roles

After creating a superuser, you can:
1. Log in to the admin panel
2. Go to Users section
3. Edit your user and set the role to 'admin', 'staff', or 'user'

## Features to Test

1. **Registration**: Create a new user account
2. **QR Code**: After registration, view your QR code in the dashboard
3. **QR Login**: Use the QR code token to login
4. **Revoke QR**: Test revoking and reactivating QR codes
5. **Admin Panel**: Manage users and QR codes
6. **Optimizer**: View system call performance data

## Troubleshooting

- **Media files not found**: Create `media/qr_codes/` directory manually
- **Static files not loading**: Run `python manage.py collectstatic`
- **Database errors**: Delete `db.sqlite3` and run migrations again

