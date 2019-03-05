from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Student
from schedule.models import Attendance, attendanceCalculator
from home.forms import SearchForm


class StudentListView(LoginRequiredMixin, ListView, FormView):
                                                                        # To List Students
    model = Student
    template_name = 'student/student.html'
    context_object_name = 'students'
    ordering = ['roll_no']
    form_class = SearchForm
    query = ""

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['pageName'] = 'Student'
        context['query'] = self.query
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query = form.cleaned_data['search']
            return Student.objects.filter(Q(roll_no__icontains=self.query) | Q(name__icontains=self.query) | Q(subject__subject__icontains=self.query) |
                                          Q(course__course__icontains=self.query)).distinct().order_by('roll_no')
        return Student.objects.all()


class StudentDetailView(LoginRequiredMixin, DetailView):
                                                                                                # To Display Student Details
    model = Student
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['pageName'] = 'student details'
        queryset = Attendance.objects.filter(student=self.object.id)
        if queryset:
            attendance = attendanceCalculator(queryset)
            context['present'] = attendance['attendancePercent']
        else:
            context['present'] = "No Attendance Data"
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
