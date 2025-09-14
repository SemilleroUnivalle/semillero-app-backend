from rest_framework import serializers
from .models import Student
import pytest

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

@pytest.mark.django_db
def test_student_serializer_valid_data():
    student_data = {
        'name': 'John Doe',
        'age': 20,
        'email': 'john.doe@example.com'
    }
    serializer = StudentSerializer(data=student_data)
    assert serializer.is_valid()
    assert serializer.validated_data['name'] == student_data['name']

@pytest.mark.django_db
def test_student_serializer_invalid_data():
    student_data = {
        'name': '',
        'age': 20,
        'email': 'john.doe@example.com'
    }
    serializer = StudentSerializer(data=student_data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors