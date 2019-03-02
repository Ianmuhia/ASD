from django.urls import path
from .views import (ScheduleListView, CheckAttendanceView, ScheduleCreateView, ScheduleDetailView,
                    ScheduleUpdateView, ScheduleDeleteView, PdfGenView)


urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule'),
    path('check/', CheckAttendanceView.as_view(), name='check-attendance'),
    path('check/pdf/<int:roll_no>/<str:start_date>/<str:end_date>/', PdfGenView.as_view(), name='pdf-gen'),
    path('new/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
]
