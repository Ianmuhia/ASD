from django.db import models
from django.urls import reverse


class Subject(models.Model):
    subject = models.CharField(max_length=250, unique=True, verbose_name='subject name')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('subject')
