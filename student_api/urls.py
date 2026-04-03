"""
student_api URL Configuration — Lab 3.2
IT322 | Student ID: 2023300660
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# ─── Swagger / OpenAPI Schema ─────────────────────────────────────────────────
schema_view = get_schema_view(
    openapi.Info(
        title="Student Management API",
        default_version='v1',
        description=(
            "## Lab 3.2 — Securing, Documenting, and Testing REST APIs\n\n"
            "**IT322 | Student ID: 2023300660**\n\n"
            "This API manages student records in a university system. "
            "All endpoints (except `/api/token/` and `/api/v1/students/health/`) "
            "require a valid JWT **Bearer** token.\n\n"
            "### How to authenticate:\n"
            "1. `POST /api/token/` with `{\"username\": \"...\", \"password\": \"...\"}`\n"
            "2. Copy the `access` token from the response.\n"
            "3. Click **Authorize** above and enter: `Bearer <access_token>`"
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="2023300660@student.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1 — Students
    path('api/v1/', include('students.urls')),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
