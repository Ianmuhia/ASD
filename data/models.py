from django.db import models
from django.urls import reverse


class Course(models.Model):
    course = models.CharField(max_length=250)

    def __str__(self):
        return self.course

    def get_absolute_url(self):
        return reverse('course')


class Subject(models.Model):
    subject = models.CharField(max_length=250)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('subject')
