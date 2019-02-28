from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .models import Course, Subject, Student, Schedule, Attendance
from .forms import SearchForm, AttendanceForm, ScheduleForm


@method_decorator(staff_member_required, name='dispatch')
class SubjectView(ListView, FormView):
                                        # To List All Subjects
    model = Subject
    template_name = 'data/course_or_subject.html'
    form_class = SearchForm
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['pageName'] = 'subject'
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Subject.objects.filter(subject__icontains=form.cleaned_data['search']).order_by('subject')
        return Subject.objects.all().order_by('subject')


@method_decorator(staff_member_required, name='dispatch')
class SubjectCreateView(CreateView):
                                        # To Create New Subject
    model = Subject
    fields = ['subject']
    template_name = 'data/course_or_subject_form.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Add New Subject'
        context['page'] = "subject"
        return context


@method_decorator(staff_member_required, name='dispatch')
class SubjectUpdateView(UpdateView):
                                        # To Update Subject
    model = Subject
    fields = ['subject']
    template_name = 'data/course_or_subject_form.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Subject'
        context['page'] = "subject"
        return context


@method_decorator(staff_member_required, name='dispatch')
class SubjectDeleteView(DeleteView):
                                        # To Delete Subject
    model = Subject
    success_url = reverse_lazy('subject')
    template_name = 'data/course_or_subject_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Subject'
        context['page'] = "subject"
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseView(ListView, FormView):
                            # To List Courses
    model = Course
    template_name = 'data/course_or_subject.html'
    context_object_name = 'courses'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['pageName'] = 'course'
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Course.objects.filter(course__icontains=form.cleaned_data['search']).order_by('course')
        return Course.objects.all().order_by('course')


@method_decorator(staff_member_required, name='dispatch')
class CourseCreateView(CreateView):
                                    # To Create New Course
    model = Course
    fields = '__all__'
    template_name = 'data/course_or_subject_form.html'

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Create Course'
        context['page'] = "course"
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseUpdateView(UpdateView):
                                    # To Update Course
    model = Course
    template_name = 'data/course_or_subject_form.html'
    fields = ['course']

    def get_context_data(self, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Course'
        context['page'] = "course"
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseDeleteView(DeleteView):
                                    # To Delete Course
    model = Course
    template_name = 'data/course_or_subject_confirm_delete.html'
    success_url = reverse_lazy('course')

    def get_context_data(self, **kwargs):
        context = super(CourseDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Course'
        context['page'] = "course"
        return context


class StudentListView(LoginRequiredMixin, ListView):
                                # To List Students
    model = Student
    template_name = 'data/student.html'
    context_object_name = 'students'
    ordering = ['roll_no']

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['pageName'] = 'Student'
        return context


@method_decorator(staff_member_required, name='dispatch')
class StudentDetailView(DetailView):
                                    # To Display Student Details
    model = Student
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['pageName'] = 'student details'
        attendance = Attendance.objects.filter(student=self.object.id)
        counter = 0
        for x in attendance:
            if x.mark:
                counter += 1
        if counter:
            context['present'] = format((counter * 100 / attendance.count()), '0.2f') + "%"
        else:
            context['present'] = 'No Attendance Registered For This Student'
        return context


@method_decorator(staff_member_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Add new student'
        return context


@method_decorator(staff_member_required, name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Add new student'
        return context


@method_decorator(staff_member_required, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student')

    def get_context_data(self, **kwargs):
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'delete student'
        return context


class ScheduleListView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'data/schedule.html'
    model = Schedule
    form_class = SearchForm
    ordering = ['lecture_no']

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        context['pageName'] = 'schedule'
        context['schedules'] = Schedule.objects.filter(teacher=self.request.user.id)
        return context


class ScheduleDetailView(LoginRequiredMixin, DetailView, FormView):
    template_name = 'data/schedule_detail.html'
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


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super(ScheduleUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Schedule'
        context['day_list'] = Schedule.objects.get(id=self.object.id).day  # fetch day list
        return context


class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Schedule'
        return context
