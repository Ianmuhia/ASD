from django.urls import path
from .views import CourseView, CourseCreateView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('', CourseView.as_view(), name='course'),
    path('new/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
]
