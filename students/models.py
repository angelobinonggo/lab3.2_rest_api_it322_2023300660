from django.db import models


class Student(models.Model):
    """
    Represents a university student record.
    """
    YEAR_CHOICES = [(i, f"Year {i}") for i in range(1, 6)]

    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    year_level = models.IntegerField(choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.student_id} — {self.full_name}"
