from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Course(models.Model):
    course = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.course

    def get_absolute_url(self):
        return reverse('course')


class Subject(models.Model):
    subject = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('subject')


class Student(models.Model):
    _1 = 'semester 1'
    _2 = 'semester 2'
    _3 = 'semester 3'
    _4 = 'semester 4'
    _5 = 'semester 5'
    _6 = 'semester 6'
    _7 = 'semester 7'
    _8 = 'semester 8'
    _9 = 'semester 9'
    _10 = 'semester 10'
    semester_choices = ((_1, 'Semester 1'), (_2, 'Semester 2'), (_3, 'Semester 3'), (_4, 'Semester 4'), (_5, 'Semester 5'),
                        (_6, 'Semester 6'), (_7, 'Semester 7'), (_8, 'Semester 8'), (_9, 'Semester 9'), (_10, 'Semester 10'),
                        )
    roll_no = models.PositiveIntegerField(validators=[MinValueValidator(1)], unique=True, blank=False)
    name = models.CharField(max_length=250, blank=False)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, default=None)
    sem = models.CharField(max_length=12, choices=semester_choices, blank=False)
    subject = models.ManyToManyField(Subject, blank=False)
    image = models.ImageField(upload_to='student_pics/', default='student_pics/default.png', max_length=500)

    def __str__(self):
        return self.name

    def get_absolute_url(self, **kwargs):
        return reverse('student-detail', kwargs={'pk': self.pk})
