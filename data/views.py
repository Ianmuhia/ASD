from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .models import Course, Subject, Student


@method_decorator(staff_member_required, name='dispatch')
class SubjectView(ListView):
                                        # To List All Subjects
    model = Subject
    template_name = 'data/course_or_subject.html'
    context_object_name = 'subjects'
    ordering = ['subject']

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['pageName'] = 'subject'
        return context


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
class CourseView(ListView):
                            # To List Courses
    model = Course
    template_name = 'data/course_or_subject.html'
    context_object_name = 'courses'
    ordering = ['course']

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['pageName'] = 'course'
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseCreateView(CreateView):
                                    # To Create New Course
    model = Course
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
