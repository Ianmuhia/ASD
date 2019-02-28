from django.contrib import admin
from .models import Course, Subject, Student, Schedule, Attendance
# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Schedule)
admin.site.register(Attendance)
