from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.db.models import Q
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .models import Subject, Course, Student, Schedule, Attendance
from .forms import AttendanceForm, ScheduleForm, CheckAttendanceForm
from home.forms import SearchForm


class ScheduleListView(LoginRequiredMixin, ListView, FormView):
    template_name = 'schedule/schedule.html'
    model = Schedule
    context_object_name = "schedules"
    form_class = SearchForm
    query = ""

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        context['pageName'] = 'schedule'
        context['query'] = self.query
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query = form.cleaned_data['search']

            if self.request.user.is_staff:
                return Schedule.objects.filter(Q(subject__subject__icontains=self.query) | Q(course__course__icontains=self.query) |
                                               Q(teacher__username__icontains=self.query)).order_by('teacher').distinct()
                # returns searched query from all teachers
            return Schedule.objects.filter(Q(teacher=self.request.user) &
                                           (Q(subject__subject__icontains=self.query) | Q(course__course__icontains=self.query))).order_by('lecture_no').distinct()
            # returns searched query with teacher = logged in teacher
        if self.request.user.is_staff:
            return Schedule.objects.all().order_by('teacher')  # returns all schedules
        return Schedule.objects.filter(teacher=self.request.user).order_by('lecture_no')  # returns all schedules with teacher = logged in teacher


class ScheduleDetailView(LoginRequiredMixin, DetailView, FormView):
    template_name = 'schedule/schedule_detail.html'
    model = Schedule
    context_object_name = 'schedule'
    form_class = AttendanceForm
    course = Course
    subject = Subject
    student = Student

    def get_context_data(self, **kwargs):
        context = super(ScheduleDetailView, self).get_context_data(**kwargs)
        context['pageName'] = 'Submit Attendance'
        global students_1
        students_1 = Student.objects.filter(course__id__in=self.object.course.all(), sem=self.object.sem, subject__id__contains=self.object.subject.id).order_by('roll_no')
        context['students'] = students_1
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            date = form.cleaned_data['lecture_date']
            x = 1
            for stu in students_1:
                lecture_v = self.model.objects.get(id=self.object.id)
                subject_v = self.subject.objects.get(id=self.object.subject.id)
                course_v = self.course.objects.get(id=stu.course.id)
                student_v = self.student.objects.get(id=stu.id)
                mark_v = mark_list = request.POST.get(f'mark{x}')
                if(not(mark_v)):
                    mark_v = 0
                attendance = Attendance(lecture=lecture_v, subject=subject_v, course=course_v, student=student_v, lecture_date=date, mark=mark_v)
                attendance.save()
                x += 1

            return redirect('schedule')


@method_decorator(staff_member_required, name='dispatch')
class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super(ScheduleCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Create Schedule'
        return context


@method_decorator(staff_member_required, name='dispatch')
class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super(ScheduleUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Schedule'
        context['day_list'] = Schedule.objects.get(id=self.object.id).day  # fetch day list
        return context


@method_decorator(staff_member_required, name='dispatch')
class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Schedule'
        return context


class CheckAttendanceView(LoginRequiredMixin, FormView, ListView):
    template_name = 'schedule/check_attendance_form.html'
    form_class = CheckAttendanceForm
    context_object_name = "attendance"
    model = Attendance
    query = ""

    def get_context_data(self, **kwargs):
        context = super(CheckAttendanceView, self).get_context_data(**kwargs)
        context['query'] = self.query
        context['pageName'] = 'Check Attendance'
        attendance = context['attendance']
        counter = 0
        for value in attendance:
            if value.mark:
                counter += 1
        context['student_name'] = Student.objects.get(id=attendance.first().student.id).name
        context['present_days'] = counter
        context['total_days'] = attendance.count()
        if counter:
            context['present'] = format((counter * 100 / attendance.count()), '0.2f') + "%"
        else:
            context['present'] = "This student didn't attended class till now."
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():

            self.query = form.cleaned_data['roll_no']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            return Attendance.objects.filter(student__roll_no=self.query, lecture_date__range=(start_date, end_date))
        return Attendance.objects.all()


class PdfGenView(TemplateView):
    model = Attendance

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        attendance = Attendance.objects.filter(student__roll_no=self.kwargs.get('roll_no'), lecture_date__range=(self.kwargs.get('start_date'), self.kwargs.get('end_date')))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        width, height = A4
        # Start writing the PDF here
        counter = 0
        for value in attendance:
            if value.mark:
                counter += 1
        student_name = Student.objects.get(id=attendance.first().student.id).name
        present_days = counter
        total_days = attendance.count()
        if counter:
            present = format((counter * 100 / attendance.count()), '0.2f') + "%"
        else:
            present = "This student didn't attended class till now."

        name = f'Name of Student : {student_name}'
        total = f'Total No. of Days : {total_days}'
        present_days = f'No. of Days Present : {present_days}'
        percent = f'Present Percentage : {present}'

        textobject = p.beginText(50, height - 50)
        textobject.setFont("Helvetica", 12)
        textobject.textLine(name)
        textobject.textLine(total)
        textobject.textLine(present_days)
        textobject.textLine(percent)
        textobject.textLine('=' * 30)
        textobject.textLine("Attended | Lecture Date")

        for x in attendance:
            if x.mark:
                text = "Present  "
            else:
                text = "Absent   "
            text += f' | {x.lecture_date}'
            textobject.textLine(text)
            text = ""

        p.drawText(textobject)

        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response
