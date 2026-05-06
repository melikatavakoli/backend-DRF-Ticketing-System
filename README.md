<div align="center">

# 🎫 Ticket Management System

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.1-red?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A **production-ready ticket management system** built with Django —  
clean, scalable, and fully containerized with Docker.

</div>

---

## 📌 About The Project

This is a complete **ticket management solution** designed for customer support, internal ticketing, or any use case requiring structured issue tracking.

### Key Features

- ✅ **Complete ticket lifecycle** — create, reply, resolve, and track
- ✅ **File attachments** with validation for each message
- ✅ **User roles & permissions** for agents and customers
- ✅ **Priority & category management** for efficient sorting
- ✅ **Seen/unseen tracking** for messages
- ✅ **Audit logging** with django-auditlog
- ✅ **History tracking** with django-simple-history
- ✅ **REST API** with DRF + JWT authentication
- ✅ **Celery** for background tasks
- ✅ **Redis** for caching and message broker
- ✅ **Docker** ready for easy deployment

---

## 🧱 Architecture Overview

```
ticket-project/
│
├── config/           # Project settings (settings.py, urls.py, wsgi.py, asgi.py)
├── common/           # Shared utilities, base models, managers, mixins
│   ├── models.py     # BaseModel with common fields
│   ├── managers.py   # Custom queryset managers
│   ├── serializers.py
│   ├── paginations.py
│   ├── filters.py
│   ├── exports.py
│   └── storage.py
│
├── core/             # User management & authentication
│   ├── models.py     # BaseUser (custom user model)
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── tasks.py
│   └── types.py      # Enums (RoleType, StatusType)
│
└── ticket/           # Main ticket application
│   ├── models.py     # Ticket & TicketDetail
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── type.py       # TicketStatus, PriorityType, TicketCategory
│   └── admin.py
```

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Django 5.1, Django REST Framework |
| **Database** | PostgreSQL 15 |
| **Cache & Broker** | Redis 7.1 |
| **Task Queue** | Celery 5.4, Celery Beat, Flower |
| **Auth** | SimpleJWT, Djoser |
| **Storage** | django-storages + S3/Boto3 |
| **Logging & Audit** | django-auditlog, django-simple-history, python-json-logger |
| **API Docs** | drf-spectacular (OpenAPI) |
| **Utils** | pandas, openpyxl, persiantools, jdatetime |
| **Deployment** | Docker, Docker Compose, Gunicorn |

---

## 🚀 Quick Start with Docker

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone git@github.com:yourusername/ticket-project.git
cd ticket-project

# Copy environment variables
cp .env.sample .env

# Build and run with Docker Compose
docker compose up --build

# Apply migrations (in another terminal)
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

Your application will be available at:
- **API:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Flower (Celery Monitor):** http://localhost:5555
- **API Docs:** http://localhost:8000/api/docs

---

## 💻 Local Development (Without Docker)

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Redis 7.1+

### Setup

```bash
# Clone the repository
git clone git@github.com:yourusername/ticket-project.git
cd ticket-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.sample .env
# Edit .env with your database credentials

# Run PostgreSQL and Redis (or install locally)
# For quick setup, use Docker for dependencies only:
docker compose up -d postgres redis

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Running Celery Workers

```bash
# Terminal 1: Celery Worker
celery -A config worker -l info

# Terminal 2: Celery Beat (scheduler)
celery -A config beat -l info

# Terminal 3: Flower (monitoring)
celery -A config flower
```

---

## 🐳 Docker Compose Services

```yaml
services:
  postgres-db   # PostgreSQL database
  redis         # Redis cache & broker
  web           # Django application (Gunicorn)
  celery-worker # Celery worker for background tasks
  celery-beat   # Celery beat for scheduled tasks
  flower        # Celery monitoring dashboard
```

---

## 📁 Environment Variables (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | development / production | ✅ |
| `DEBUG` | True / False | ✅ |
| `DJANGO_SECRET_KEY` | Django secret key | ✅ |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | ✅ |
| `POSTGRES_DB` | Database name | ✅ |
| `POSTGRES_USER` | Database user | ✅ |
| `POSTGRES_PASSWORD` | Database password | ✅ |
| `POSTGRES_HOST` | Database host | ✅ |
| `POSTGRES_PORT` | Database port | ✅ |
| `REDIS_URL` | Redis connection URL | ✅ |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | JWT access token lifetime | ❌ |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | JWT refresh token lifetime | ❌ |

---

**Authentication:** JWT Bearer token required for all endpoints except public ones.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific app tests
pytest ticket/
pytest core/

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## 📊 Monitoring & Logging

- **Celery Flower:** `http://localhost:5555` — Monitor tasks and workers
- **Django Debug Toolbar:** Available in development mode
- **Structured Logging:** JSON logs for production
- **Audit Log:** All model changes are tracked automatically

---

## 🚢 Deployment

### Production Checklist

1. ✅ Set `ENVIRONMENT=production`
2. ✅ Set `DEBUG=False`
3. ✅ Use strong `DJANGO_SECRET_KEY`
4. ✅ Configure proper `ALLOWED_HOSTS`
5. ✅ Use PostgreSQL (not SQLite)
6. ✅ Set up Redis for caching
7. ✅ Configure static files storage (S3/CloudFront)
8. ✅ Enable HTTPS
9. ✅ Set up database backups

### Docker Production Build

```bash
# Build with production settings
docker compose -f docker-compose.prod.yml up --build -d

# Apply migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

---

## 📄 License

This project is open source under the **MIT License**.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📞 Contact

**Developer:** Melika Tavakoli

---

<div align="center">

⭐ **Star this repo** if you find it useful!

🐛 **Issues & PRs** welcome — let's build better ticketing systems together.

</div>
```
