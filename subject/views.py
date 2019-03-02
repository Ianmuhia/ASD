from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .models import Subject
from home.forms import SearchForm


@method_decorator(staff_member_required, name='dispatch')
class SubjectView(ListView, FormView):
                                        # To List All Subjects
    model = Subject
    template_name = 'subject/subject.html'
    form_class = SearchForm
    context_object_name = 'subjects'
    query = ""

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query = form.cleaned_data['search']
            return Subject.objects.filter(subject__icontains=self.query).order_by('subject')
        return Subject.objects.all().order_by('subject')

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['pageName'] = 'subject'
        context['query'] = self.query
        return context


@method_decorator(staff_member_required, name='dispatch')
class SubjectCreateView(CreateView):
                                        # To Create New Subject
    model = Subject
    fields = ['subject']

    def get_context_data(self, **kwargs):
        context = super(SubjectCreateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Add New Subject'
        return context


@method_decorator(staff_member_required, name='dispatch')
class SubjectUpdateView(UpdateView):
                                        # To Update Subject
    model = Subject
    fields = ['subject']

    def get_context_data(self, **kwargs):
        context = super(SubjectUpdateView, self).get_context_data(**kwargs)
        context['pageName'] = 'Update Subject'
        return context


@method_decorator(staff_member_required, name='dispatch')
class SubjectDeleteView(DeleteView):
                                        # To Delete Subject
    model = Subject
    success_url = reverse_lazy('subject')

    def get_context_data(self, **kwargs):
        context = super(SubjectDeleteView, self).get_context_data(**kwargs)
        context['pageName'] = 'Delete Subject'
        return context
