from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'course', 'year_level', 'created_at')
    list_filter = ('course', 'year_level')
    search_fields = ('student_id', 'full_name', 'email')
    ordering = ('student_id',)
    readonly_fields = ('created_at', 'updated_at')
