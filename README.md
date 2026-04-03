# Lab 3.2 — Securing, Documenting & Testing REST APIs

**IT322 | Student ID: 2023300660**

A fully-secured Student Management REST API built with **Django REST Framework**, protected by **JWT authentication**, documented with **Swagger/OpenAPI**, and equipped with structured logging.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Seed sample data (optional)
python manage.py seed_students

# 4. Create admin user (if not already created)
python manage.py createsuperuser

# 5. Start the development server
python manage.py runserver
```

---

## 🔗 Available URLs

| URL | Description |
|-----|-------------|
| `http://localhost:8000/swagger/` | **Swagger UI** — interactive docs |
| `http://localhost:8000/redoc/` | ReDoc documentation |
| `http://localhost:8000/swagger.json` | OpenAPI JSON schema |
| `http://localhost:8000/admin/` | Django admin panel |
| `http://localhost:8000/api/token/` | Obtain JWT token (POST) |
| `http://localhost:8000/api/token/refresh/` | Refresh JWT token (POST) |
| `http://localhost:8000/api/v1/students/` | Student list / create |
| `http://localhost:8000/api/v1/students/{id}/` | Student retrieve / update / delete |
| `http://localhost:8000/api/v1/students/health/` | Health check (no auth required) |

---

## 🔐 Part A: JWT Authentication

### Step 1 — Obtain a token

```bash
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin1234"
}
```

**Response:**
```json
{
  "access": "<your_access_token>",
  "refresh": "<your_refresh_token>"
}
```

### Step 2 — Use the token

Add to every request header:
```
Authorization: Bearer <your_access_token>
```

### Step 3 — Refresh when expired

```bash
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "<your_refresh_token>"
}
```

---

## 📚 Part B: API Endpoints

All endpoints (except `/health/`) require `Authorization: Bearer <token>`.

### Students Resource — `/api/v1/students/`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/students/` | List all students (paginated) | ✅ |
| POST | `/api/v1/students/` | Create a new student | ✅ |
| GET | `/api/v1/students/{id}/` | Retrieve a student by ID | ✅ |
| PUT | `/api/v1/students/{id}/` | Fully update a student | ✅ |
| PATCH | `/api/v1/students/{id}/` | Partially update a student | ✅ |
| DELETE | `/api/v1/students/{id}/` | Delete a student | ✅ |
| GET | `/api/v1/students/health/` | API health check | ❌ (public) |

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `search` | Search by name, email, course, student_id | `?search=juan` |
| `course` | Filter by course | `?course=BSIT` |
| `year_level` | Filter by year level (1–5) | `?year_level=3` |
| `ordering` | Sort results | `?ordering=full_name` |
| `page` | Pagination page number | `?page=2` |
| `page_size` | Results per page | `?page_size=5` |

### Sample Request Body (POST/PUT)

```json
{
  "student_id": "2024-001",
  "full_name": "Juan Dela Cruz",
  "email": "juan@student.edu",
  "course": "BSIT",
  "year_level": 3
}
```

### Sample Success Response (201 Created)

```json
{
  "id": 1,
  "student_id": "2024-001",
  "full_name": "Juan Dela Cruz",
  "email": "juan@student.edu",
  "course": "BSIT",
  "year_level": 3,
  "created_at": "2026-04-03T01:00:00.000000+08:00",
  "updated_at": "2026-04-03T01:00:00.000000+08:00"
}
```

### Error Response (401 Unauthorized)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 📄 Part C: API Documentation (Swagger)

Visit: **http://localhost:8000/swagger/**

To test authenticated endpoints in Swagger:
1. Open `/swagger/`
2. Click **Authorize** (lock icon)
3. Enter: `Bearer <your_access_token>`
4. Click **Authorize**, then explore endpoints

---

## 🧪 Part D: Testing and Debugging

### Types of Testing Applied

| Type | Tool | What is tested |
|------|------|----------------|
| **Functional Testing** | Postman / Swagger UI | Correct HTTP status codes (200, 201, 401, 404) |
| **Security Testing** | Postman | Unauthorized access returns 401 |
| **Unit / Integration** | Django test runner | Serializer validation, model constraints |

### Functional Testing Checklist (Postman)

- [x] `GET /api/v1/students/` → 200 OK with paginated list
- [x] `POST /api/v1/students/` → 201 Created with new student
- [x] `GET /api/v1/students/{id}/` → 200 OK or 404 Not Found
- [x] `PUT /api/v1/students/{id}/` → 200 OK with updated student
- [x] `PATCH /api/v1/students/{id}/` → 200 OK with partial update
- [x] `DELETE /api/v1/students/{id}/` → 204 No Content
- [x] Any endpoint without token → 401 Unauthorized

### Debugging Technique Used

**Structured Logging** — every request is logged with:
- Action type (LIST, CREATE, RETRIEVE, UPDATE, DELETE)
- User making the request
- Student ID being accessed

Log output is written to both the console and `api.log` in the project root.

---

## 📋 HTTP Status Codes Reference

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET / PUT / PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing or invalid JWT |
| 403 | Forbidden | Valid token but no permission |
| 404 | Not Found | Resource does not exist |
| 500 | Server Error | Unhandled exception |

---

## 🛠 Tech Stack

- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Auth**: djangorestframework-simplejwt
- **Docs**: drf-yasg (Swagger / OpenAPI)
- **DB**: SQLite (development)
- **Logging**: Python `logging` module (console + file)

---

## 💭 Reflection

This lab gave me a deeper understanding of how REST APIs are secured, documented, and tested in a real-world setting. Implementing JWT (JSON Web Token) authentication showed me how stateless token-based security works — instead of storing session data on the server, the client carries a signed token with every request, which the server validates independently, making the API more scalable and aligned with REST's stateless principle. Generating API documentation using Swagger (drf-yasg) was particularly valuable, as I learned how self-documenting APIs reduce friction for developers trying to integrate with the system — the interactive Swagger UI allowed me to test endpoints directly without needing a separate tool. During security testing, observing the `401 Unauthorized` response when accessing a protected endpoint without a token confirmed that the authentication layer was working correctly, and reinforced why proper access control is non-negotiable in any production API. Setting up structured logging in the ViewSet also highlighted how crucial visibility is during debugging — by capturing who made each request and what resource was accessed, issues can be traced quickly without guesswork. Overall, this lab demonstrated that building a REST API is not just about making endpoints work, but about making them secure, understandable, and maintainable for both developers and end users.
