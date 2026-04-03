from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Handles validation and conversion between Python objects and JSON.
    """

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_year_level(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Year level must be between 1 and 5.")
        return value

    def validate_student_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("Student ID cannot be blank.")
        return value.upper()
