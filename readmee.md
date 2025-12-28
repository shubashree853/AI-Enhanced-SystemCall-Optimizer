# AI-Enhanced System Call Optimizer

A Django-based real-time system call monitoring and optimization tool with **AI-powered recommendations** using **Groq API** for performance analysis and smart optimization strategies.

![Performance-Metrics](./static/images/Screenshot%20from%202025-04-05%2014-50-08.png)
![Interface](./static/images/Screenshot%20from%202025-04-05%2014-50-20.png)
![Optimization-Recommendations](./static/images/Screenshot%20from%202025-04-05%2014-50-23.png)

## 🙏 Special Thanks

This project is a recreation and enhancement of the original **AI System Call Optimizer** project. Special thanks to the original repository:

**Original Repository:** [https://github.com/CipherYuvraj/AI-Enhanced-System-Call-Optimization](https://github.com/CipherYuvraj/AI-Enhanced-System-Call-Optimization)

The original project provided the foundation for system call monitoring using **eBPF**, **Flask**, and **AI (Groq API)**. This Django-based version extends the functionality with:

- Enhanced user authentication with QR code login
- Role-based access control
- Activity logging and reporting
- Improved web interface with Bootstrap
- Better session management
- Comprehensive dashboard with real-time metrics

For Linux system requirements and eBPF-based monitoring, please refer to the original repository's documentation on **AI System Call Optimizer** - a real-time system call monitoring and optimization tool using eBPF, Flask, and optional AI (Groq API) for performance analysis and smart recommendations.

## 📌 Features

- 🟢 Real-time system call monitoring and performance tracking
- 📊 Execution time & resource metrics (CPU, memory, I/O)
- 📁 Categorization of syscalls: File I/O, Process, Memory, IPC, etc.
- 🤖 AI-generated optimization tips using Groq API
- 🛠️ Rule-based fallback suggestions when AI is unavailable
- 🌐 Modern Django web UI with auto-refresh
- 🔍 RESTful API endpoints for programmatic access
- 🔐 User authentication with QR code login support
- 👥 Role-based access control (Admin, Staff, User)
- 📝 Comprehensive activity logging and reporting
- 📈 Real-time dashboard with performance trends

---

## ⚙️ System Requirements

### For Django Application (Windows/Linux/Mac):
- Python 3.8+
- Django 4.2+
- SQLite (default) or PostgreSQL/MySQL for production

### For eBPF Monitoring (Linux only):
- Linux with eBPF support (Kernel ≥ 4.1)
- BCC (BPF Compiler Collection) - Optional, for kernel-level monitoring
- Root/sudo access for eBPF probes

> **Note**: The Django application can run on any platform. eBPF monitoring features require Linux with appropriate kernel support.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-enhanced-system-call-optimization.git
cd ai-enhanced-system-call-optimization
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Groq API (Optional - for AI recommendations)
GROQ_API_KEY=your_groq_api_key_here

# Database (Optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Usage

### 1. Start the Django Development Server

```bash
python manage.py runserver
```

The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Access the Application

- **Home Page**: `http://127.0.0.1:8000/`
- **Register**: `http://127.0.0.1:8000/register/`
- **Login**: `http://127.0.0.1:8000/login/`
- **QR Code Login**: `http://127.0.0.1:8000/qr-login/`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/` (requires login)
- **Optimizer**: `http://127.0.0.1:8000/optimizer/` (requires login)
- **Admin Panel**: `http://127.0.0.1:8000/admin/` (requires superuser)

### 3. Set the Groq API Key (Optional)

To enable AI-powered optimization recommendations:

```bash
# In .env file:
GROQ_API_KEY=your_api_key_here

# Or export as environment variable:
export GROQ_API_KEY=your_api_key_here
```

Without the API key, the system will use rule-based fallback recommendations.

---

## 🔌 API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register/` | POST | User registration |
| `/login/` | POST | Traditional username/password login |
| `/api/qr-login/` | POST | QR code authentication |
| `/logout/` | GET | User logout |

### Optimizer Endpoints (Requires Authentication)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/optimizer/` | GET | Optimizer dashboard |
| `/optimizer/performance/` | GET | Get live syscall performance data |
| `/optimizer/recommendations/` | GET | Get AI-based or rule-based optimization suggestions |
| `/optimizer/categories/` | GET | View syscall categories and groupings |
| `/optimizer/syscall/<syscall_name>/` | GET | Get detailed metrics for a specific syscall |
| `/optimizer/generate-fake-data/` | POST | Generate sample system call data for testing |

### User Management Endpoints (Requires Authentication)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard/` | GET | User dashboard |
| `/activity-logs/` | GET | View user activity logs |
| `/reports/` | GET | View activity reports |
| `/export-report/` | GET | Export activity report as CSV |
| `/generate-qr/` | GET | Generate/regenerate QR code |
| `/revoke-qr/` | GET | Revoke QR code |
| `/activate-qr/` | GET | Activate QR code |

### Example API Usage

```bash
# Get performance data (requires authentication)
curl -H "Cookie: sessionid=your_session_id" http://127.0.0.1:8000/optimizer/performance/

# Get recommendations
curl -H "Cookie: sessionid=your_session_id" http://127.0.0.1:8000/optimizer/recommendations/

# Get specific syscall details
curl -H "Cookie: sessionid=your_session_id" http://127.0.0.1:8000/optimizer/syscall/write/
```

---

## 🛠️ Configuration

### Django Settings

Edit `syscall_optimizer/settings.py`:

- **SECRET_KEY**: Change in production
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Add your domain for production
- **DATABASES**: Configure for PostgreSQL/MySQL in production

### Optimizer Settings

Edit `optimizer/optimizer.py`:

- **performance_threshold**: Default `0.05s` - threshold for flagging slow syscalls
- **learning_rate**: Default `0.1` - learning rate for optimization algorithms
- **refresh_interval**: Default `5` seconds - dashboard auto-refresh interval

### Groq API Configuration

1. Sign up at [https://console.groq.com/](https://console.groq.com/)
2. Get your API key
3. Add to `.env` file: `GROQ_API_KEY=your_key_here`

---

## ⚡ Performance Considerations

- Django application overhead is minimal
- Groq API calls are async/lightweight and do not block real-time monitoring
- SQLite is suitable for development; use PostgreSQL/MySQL for production
- For high-traffic scenarios, consider:
  - Database connection pooling
  - Redis for session storage
  - Caching for frequently accessed data

---

## 🔒 Security

### Production Checklist

- [ ] Change `SECRET_KEY` in `settings.py`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS/SSL certificates
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure secure session cookies
- [ ] Enable CSRF protection (already enabled)
- [ ] Use environment variables for sensitive data
- [ ] Regularly update dependencies

### QR Code Security

- QR codes contain username and token pairs
- Tokens are unique and can be revoked
- QR codes should be kept secure
- Regenerate QR codes if compromised

---

## 📁 Project Structure

```
ai-enhanced-system-call-optimization/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
│
├── syscall_optimizer/        # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
│
├── users/                    # User management app
│   ├── models.py            # User, QRCode, ActivityLog models
│   ├── views.py             # Authentication and user views
│   ├── forms.py             # User registration forms
│   ├── urls.py              # User app URLs
│   └── migrations/          # Database migrations
│
├── optimizer/                # System call optimizer app
│   ├── optimizer.py         # Core optimization engine
│   ├── views.py             # Optimizer views and API
│   ├── urls.py              # Optimizer app URLs
│   └── admin.py             # Admin configuration
│
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── users/               # User-related templates
│   └── optimizer/           # Optimizer templates
│
└── static/                   # Static files (CSS, JS, images)
```

---

## 🤝 Contributing

We love contributions! Here's how to get started:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-name`)
6. Open a Pull Request 🚀

You can also:
- Open Issues for bugs or feature suggestions
- Discuss ideas via GitHub Discussions
- Improve documentation

---

## 📄 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for full details.

---

## 📝 Additional Notes

### Dependencies

Key packages in `requirements.txt`:

```
Django>=4.2.0
groq>=0.4.0
psutil>=5.9.0
numpy>=1.24.0
python-dotenv>=1.0.0
Pillow>=10.0.0
qrcode>=7.4.0
```

### Development

For development with hot-reload:

```bash
python manage.py runserver --noreload
```

### Testing

Run tests (when available):

```bash
python manage.py test
```

### Database Reset

To reset the database:

```bash
python manage.py flush
python manage.py migrate
```

---

## 🔗 References

- **Original Project**: [AI-Enhanced-System-Call-Optimization](https://github.com/CipherYuvraj/AI-Enhanced-System-Call-Optimization)
- **Django Documentation**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **Groq API**: [https://console.groq.com/](https://console.groq.com/)
- **BCC (eBPF)**: [https://github.com/iovisor/bcc](https://github.com/iovisor/bcc)

---

**Created by**: Nandan A M  
**Version**: 1.0  
**Last Updated**: December 2025
