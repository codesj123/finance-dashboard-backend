# Finance Dashboard Backend

A Django REST Framework backend for a finance dashboard system with role-based access control (RBAC), JWT authentication, transaction management, and dashboard analytics.

---

## Tech Stack

- **Python** 3.12
- **Django** 4.x
- **Django REST Framework**
- **djangorestframework-simplejwt** — JWT authentication
- **SQLite** — database

---

## Project Structure

```
project/
├── manage.py
├── project/                  ← config
│   ├── settings.py
│   ├── urls.py
│   └── exceptions.py         ← custom error handler
├── users/                    ← authentication + RBAC
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
└── finance/                  ← transactions + dashboard
    ├── models.py
    ├── serializers.py
    ├── pagination.py
    ├── views.py
    └── urls.py
```

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd project
```

**2. Install dependencies**
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

**3. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**4. Create a superuser**
```bash
python manage.py createsuperuser
```

**5. Set the superuser role to admin**
```bash
python manage.py shell
```
```python
from users.models import User
u = User.objects.get(username='yourusername')
u.role = 'admin'
u.save()
exit()
```

**6. Start the server**
```bash
python manage.py runserver
```

---

## Authentication

This API uses JWT (JSON Web Tokens). Every request to a protected endpoint must include the access token in the `Authorization` header.

**Login**
```
POST /api/token/
Body: { "username": "...", "password": "..." }
```

**Refresh token**
```
POST /api/token/refresh/
Body: { "refresh": "..." }
```

**Using the token**
```
Authorization: Bearer <access_token>
```

Access tokens expire after **30 minutes**. Use the refresh token to get a new one without logging in again.

---

## Roles (RBAC)

| Role | What they can do |
|------|-----------------|
| `visitor` | View transactions and summary |
| `analyst` | View transactions, summary, and analytics |
| `admin` | Full access — create, update, delete transactions and manage users |

---

## API Endpoints

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/token/` | Login — returns access + refresh tokens |
| POST | `/api/token/refresh/` | Get new access token |

### Transactions
| Method | URL | Permission | Description |
|--------|-----|-----------|-------------|
| GET | `/api/transactions/` | Any role | List all transactions |
| POST | `/api/transactions/` | Admin only | Create a transaction |
| GET | `/api/transactions/<id>/` | Any role | Get one transaction |
| PUT | `/api/transactions/<id>/` | Admin only | Update a transaction |
| DELETE | `/api/transactions/<id>/` | Admin only | Soft delete a transaction |

### Dashboard
| Method | URL | Permission | Description |
|--------|-----|-----------|-------------|
| GET | `/api/summary/` | Any role | Total income, expenses, net balance, category breakdown, recent 5 |
| GET | `/api/analytics/` | Analyst + Admin | Monthly income/expense trends |

### Users
| Method | URL | Permission | Description |
|--------|-----|-----------|-------------|
| GET | `/api/users/` | Admin only | List all users |
| POST | `/api/users/` | Admin only | Create a user and assign role |
| GET | `/api/users/<id>/` | Admin only | Get a specific user |
| PUT | `/api/users/<id>/` | Admin only | Update role or deactivate |

---

## Filtering & Pagination

Transactions support filtering via query parameters:

```
GET /api/transactions/?type=income
GET /api/transactions/?category=salary
GET /api/transactions/?from=2025-01-01&to=2025-03-31
GET /api/transactions/?ordering=-amount
GET /api/transactions/?page=2&page_size=10
```

Pagination response format:
```json
{
  "total": 87,
  "pages": 5,
  "current": 1,
  "next": "http://localhost:8000/api/transactions/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "success": false,
  "status_code": 400,
  "errors": {
    "amount": ["Amount must be greater than zero."]
  }
}
```

---

## Assumptions

- Soft delete is used for transactions — records are never permanently removed to preserve audit history
- The `visitor` role can read all transactions and the summary dashboard
- Only `admin` can create, update, or delete transactions and manage users
- JWT access tokens expire in 30 minutes, refresh tokens expire in 1 day
- SQLite is used for simplicity — can be swapped for PostgreSQL in production

---

## Sample Request — Create Transaction

```bash
curl -X POST http://127.0.0.1:8000/api/transactions/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": "5000.00",
       "type": "income",
       "category": "salary",
       "date": "2025-04-01",
       "notes": "April salary"
     }'
```

Response:
```json
{
  "id": 1,
  "amount": "5000.00",
  "type": "income",
  "category": "salary",
  "date": "2025-04-01",
  "notes": "April salary",
  "created_by_username": "sj",
  "created_at": "2026-04-05T12:53:15Z"
}
```
