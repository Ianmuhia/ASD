from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
from subject.models import Subject
from course.models import Course
from student.models import Student, sem


class Schedule(models.Model):
    lecture_no = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    course = models.ManyToManyField(Course)
    sem = models.CharField(max_length=12, choices=sem(), blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=42, default=None)

    def __str__(self):
        return f'{self.lecture_no}'

    def get_absolute_url(self, **kwargs):
        return reverse('schedule-detail', kwargs={'pk': self.pk})


class Attendance(models.Model):

    lecture = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture_date = models.DateField(default=datetime.date.today)
    mark = models.BooleanField()

    def __str__(self):
        return f'Roll no : {self.student.roll_no}, Date : {self.lecture_date}'


def attendanceCalculator(queryset):  # For calculating attendance details of student
    pDays = 0
    detailList = []
    for query in queryset:
        if query.mark:
            pDays += 1
            detailList.append({"attend": "Present", "date": query.lecture_date})
        else:
            detailList.append({"attend": "Absent ", "date": query.lecture_date})

    sName = Student.objects.get(id=queryset.first().student.id).name
    tDays = queryset.count()
    if pDays:
        attendancePercent = format((pDays * 100 / tDays), '0.2f') + "%"
    else:
        attendancePercent = "This student didn't attend class till now."
    data = {'name': sName, 'presentDays': pDays, 'totalDays': tDays, 'attendancePercent': attendancePercent, 'detail': detailList}
    return data


def pdfGen(queryset):  # For Genrating Pdf file of student attendance

    attendance = queryset
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    width, height = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance-of-{attendance["name"]}.pdf"'
    name = f'Name of Student : {attendance["name"]}'
    total = f'Total No. of Days : {attendance["totalDays"]}'
    presentDays = f'No. of Days Present : {attendance["presentDays"]}'
    percent = f'Present Percentage : {attendance["attendancePercent"]}'

    textobject = p.beginText(50, height - 50)  # begin from top left
    textobject.setFont("Helvetica", 12)
    textobject.textLine(name)
    textobject.textLine(total)
    textobject.textLine(presentDays)
    textobject.textLine(percent)
    textobject.textLine('=' * 30)
    textobject.textLine("Attended | Lecture Date")

    for value in attendance['detail']:
        text = f'{value["attend"]}   |   {value["date"]}'
        textobject.textLine(text)
        text = ""

    p.drawText(textobject)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
