from django.forms import ModelForm
from .models import Course, Subject


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['subject']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course']
