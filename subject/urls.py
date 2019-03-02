from django.urls import path
from .views import SubjectView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView

urlpatterns = [
    path('', SubjectView.as_view(), name='subject'),
    path('new/', SubjectCreateView.as_view(), name='subject-create'),
    path('<int:pk>/update/', SubjectUpdateView.as_view(), name='subject-update'),
    path('<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject-delete'),
]
