from django.urls import path
from .views import StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView

urlpatterns = [
    path('', StudentListView.as_view(), name='student'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('new/', StudentCreateView.as_view(), name='student-create'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
