from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .models import Course
from home.forms import SearchForm


@method_decorator(staff_member_required, name='dispatch')
class CourseView(ListView, FormView):
                            # To List Courses
    model = Course
    template_name = 'course/course.html'
    context_object_name = 'courses'
    form_class = SearchForm
    query = ""

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['pageName'] = 'course'
        context['query'] = self.query
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query = form.cleaned_data['search']
            return Course.objects.filter(course__icontains=self.query).order_by('course')
        return Course.objects.all().order_by('course')


@method_decorator(staff_member_required, name='dispatch')
class CourseCreateView(CreateView):
                                    # To Create New Course
    model = Course
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Create Course'
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseUpdateView(UpdateView):
                                    # To Update Course
    model = Course
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Course'
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseDeleteView(DeleteView):
                                    # To Delete Course
    model = Course
    success_url = reverse_lazy('course')

    def get_context_data(self, **kwargs):
        context = super(CourseDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Course'
        return context
