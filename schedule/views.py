from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Subject, Course, Student, Schedule, Attendance, attendanceCalculator, pdfGen
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


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'schedule/schedule_detail.html'
    model = Schedule
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(ScheduleDetailView, self).get_context_data(**kwargs)
        context['pageName'] = 'Submit Attendance'
        return context


class SubmitAttendanceView(View):
    template_name = 'schedule/submit_attendance.html'  # this html file will be included in 'schedule/scheduledetail.html'
    form_class = AttendanceForm

    def get_schedule(self, value):
        return get_object_or_404(Schedule, id=value)

    def get_students(self, value):
        schedule = self.get_schedule(value)
        # specify Students queryset
        students_queryset = Student.objects.filter(course__id__in=schedule.course.all(), sem=schedule.sem, subject__id__contains=schedule.subject.id).order_by('roll_no')
        return students_queryset

    def get(self, request, **kwargs):
        form = self.form_class()
        students = self.get_students(kwargs['pk'])
        return render(request, self.template_name, {'form': form, 'students': students})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data['lecture_date']
            schedule = self.get_schedule(kwargs['pk'])
            lecture = Schedule.objects.get(id=schedule.id)
            subject = Subject.objects.get(id=schedule.subject.id)
            x = 1  # a counter to fetch each checkbox from template by their name
            students = self.get_students(kwargs['pk'])
            if students:
                for student in students:
                    course = Course.objects.get(id=student.course.id)
                    mark = self.request.POST.get(f'mark{x}')
                    if not mark:  # unchecked boxes in submit attendance
                        mark = 0
                    attendance = Attendance(lecture=lecture, subject=subject, course=course, student=student, lecture_date=date, mark=mark)
                    attendance.save()
                    x += 1
                return redirect('schedule')
        return render(request, self.template_name, {'form': form, 'students': students})


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

            return render(request, self.template_name, {'attendance': attendance, 'notFound': notFound, 'form': form, 'roll_no': roll_no})

        form = self.form_class  # if form not valid

        return render(request, self.template_name, {'form': form})


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
