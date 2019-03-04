from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Subject, Course, Student, Schedule, Attendance, attendanceCalculator, pdfGen
from .forms import AttendanceForm, ScheduleForm, CheckAttendanceForm
from home.forms import SearchForm
from django import forms


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
                mark_v = request.POST.get(f'mark{x}')
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
        context['day_list'] = Schedule.objects.get(id=self.object.id).day  # fetch day list and check already selected days
        return context


@method_decorator(staff_member_required, name='dispatch')
class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Schedule'
        return context


class CheckAttendanceView(LoginRequiredMixin, View):
    form_class = CheckAttendanceForm
    template_name = "schedule/check_attendance_form.html"

    def get(self, request, *args, **kwargs):
        attendance = ""
        notFound = ""
        form = self.form_class(self.request.GET)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if start_date > end_date:
                notFound = "' From Date ' Cannot Be Greater Than ' To Date '"  # error

            else:
                queryset = Attendance.objects.filter(student__roll_no=roll_no, lecture_date__range=(start_date, end_date))

                if queryset:
                    attendance = attendanceCalculator(queryset)  # from .models

                    if 'pdf-gen' in self.request.GET:  # if user clicked on Genrate Pdf
                        response = pdfGen(attendance)  # from .models
                        return response
                else:
                    notFound = "No Content Found"

            return render(request, self.template_name, {'attendance': attendance, 'notFound': notFound, 'form': form})

        form = self.form_class  # if form not valid

        return render(request, self.template_name, {'form': form})
