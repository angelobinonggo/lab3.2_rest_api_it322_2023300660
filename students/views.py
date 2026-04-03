import logging
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Student
from .serializers import StudentSerializer

logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Student records.

    Provides full CRUD operations:
      - list:    GET  /api/v1/students/
      - create:  POST /api/v1/students/
      - retrieve: GET  /api/v1/students/{id}/
      - update:  PUT  /api/v1/students/{id}/
      - partial_update: PATCH /api/v1/students/{id}/
      - destroy: DELETE /api/v1/students/{id}/

    All endpoints require a valid JWT Bearer token.
    Supports filtering by course and year_level, and search by name/email.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'course', 'student_id']
    ordering_fields = ['student_id', 'full_name', 'year_level', 'created_at']
    ordering = ['student_id']

    # ── Swagger parameter definitions ─────────────────────────────────────────
    _search_param = openapi.Parameter(
        'search', openapi.IN_QUERY,
        description="Search by name, email, course, or student_id",
        type=openapi.TYPE_STRING,
    )
    _course_param = openapi.Parameter(
        'course', openapi.IN_QUERY,
        description="Filter by course (e.g. BSIT)",
        type=openapi.TYPE_STRING,
    )
    _year_param = openapi.Parameter(
        'year_level', openapi.IN_QUERY,
        description="Filter by year level (1–5)",
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        operation_summary="List all students",
        operation_description=(
            "Returns a paginated list of all students. "
            "Supports ?search=, ?course=, ?year_level=, and ?ordering= query parameters."
        ),
        manual_parameters=[_search_param, _course_param, _year_param],
        security=[{'Bearer': []}],
    )
    def list(self, request, *args, **kwargs):
        logger.info(
            f"[LIST] Students requested by user '{request.user}' | "
            f"query_params={dict(request.query_params)}"
        )
        # Optional: filter by course / year_level via query params
        course = request.query_params.get('course')
        year_level = request.query_params.get('year_level')
        qs = self.get_queryset()
        if course:
            qs = qs.filter(course__iexact=course)
        if year_level:
            qs = qs.filter(year_level=year_level)
        self.queryset = qs
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new student",
        operation_description="Creates a new student record. Requires all mandatory fields.",
        security=[{'Bearer': []}],
        request_body=StudentSerializer,
        responses={
            201: StudentSerializer,
            400: "Validation error",
            401: "Unauthorized — JWT token missing or invalid",
        },
    )
    def create(self, request, *args, **kwargs):
        logger.info(f"[CREATE] New student creation attempt by '{request.user}'")
        response = super().create(request, *args, **kwargs)
        logger.info(f"[CREATE] Student created: {response.data.get('student_id')}")
        return response

    @swagger_auto_schema(
        operation_summary="Retrieve a student",
        operation_description="Returns a single student record by its database ID.",
        security=[{'Bearer': []}],
        responses={
            200: StudentSerializer,
            404: "Student not found",
            401: "Unauthorized",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"[RETRIEVE] Student id={kwargs.get('pk')} accessed by '{request.user}'")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fully update a student",
        operation_description="Replaces all fields of a student record (PUT).",
        security=[{'Bearer': []}],
        request_body=StudentSerializer,
        responses={200: StudentSerializer, 400: "Validation error", 404: "Not found"},
    )
    def update(self, request, *args, **kwargs):
        logger.info(f"[UPDATE] Student id={kwargs.get('pk')} updated by '{request.user}'")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a student",
        operation_description="Updates one or more fields of a student record (PATCH).",
        security=[{'Bearer': []}],
        request_body=StudentSerializer,
        responses={200: StudentSerializer, 400: "Validation error", 404: "Not found"},
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info(f"[PATCH] Student id={kwargs.get('pk')} partially updated by '{request.user}'")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a student",
        operation_description="Permanently removes a student record.",
        security=[{'Bearer': []}],
        responses={204: "Deleted", 404: "Not found", 401: "Unauthorized"},
    )
    def destroy(self, request, *args, **kwargs):
        logger.warning(f"[DELETE] Student id={kwargs.get('pk')} deleted by '{request.user}'")
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='get',
        operation_summary="Health check",
        operation_description="Returns API status. No authentication required.",
        security=[],
        responses={200: openapi.Response('OK', examples={'application/json': {'status': 'ok'}})},
    )
    @action(detail=False, methods=['get'], permission_classes=[], url_path='health')
    def health(self, request):
        """Public health-check endpoint — no token required."""
        logger.debug("[HEALTH] Health check called")
        return Response({'status': 'ok', 'api': 'Student Management API v1'})
