"""
Custom management command: seed_students
Usage: python manage.py seed_students

Populates the database with 10 sample students for demo/testing.
"""

from django.core.management.base import BaseCommand
from students.models import Student


SAMPLE_STUDENTS = [
    {"student_id": "2023-001", "full_name": "Juan Dela Cruz",     "email": "juan@student.edu",     "course": "BSIT",  "year_level": 3},
    {"student_id": "2023-002", "full_name": "Maria Santos",       "email": "maria@student.edu",    "course": "BSCS",  "year_level": 2},
    {"student_id": "2023-003", "full_name": "Pedro Reyes",        "email": "pedro@student.edu",    "course": "BSIT",  "year_level": 4},
    {"student_id": "2023-004", "full_name": "Ana Gonzalez",       "email": "ana@student.edu",      "course": "BSIS",  "year_level": 1},
    {"student_id": "2023-005", "full_name": "Carlos Mendoza",     "email": "carlos@student.edu",   "course": "BSCE",  "year_level": 5},
    {"student_id": "2023-006", "full_name": "Liza Villanueva",    "email": "liza@student.edu",     "course": "BSIT",  "year_level": 2},
    {"student_id": "2023-007", "full_name": "Miguel Fernandez",   "email": "miguel@student.edu",   "course": "BSCS",  "year_level": 3},
    {"student_id": "2023-008", "full_name": "Sofia Ramos",        "email": "sofia@student.edu",    "course": "BSIS",  "year_level": 4},
    {"student_id": "2023-009", "full_name": "Rafael Torres",      "email": "rafael@student.edu",   "course": "BSCE",  "year_level": 1},
    {"student_id": "2023-010", "full_name": "Gabriela Cruz",      "email": "gabriela@student.edu", "course": "BSIT",  "year_level": 5},
]


class Command(BaseCommand):
    help = "Seeds the database with 10 sample student records."

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0
        for data in SAMPLE_STUDENTS:
            obj, was_created = Student.objects.get_or_create(
                student_id=data["student_id"],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✔ Created: {obj}"))
            else:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"  ⚠ Skipped (exists): {obj}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {created} student(s) created, {skipped} skipped."
            )
        )
