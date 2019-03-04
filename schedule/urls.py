from django.urls import path
from .views import (ScheduleListView, CheckAttendanceView, ScheduleCreateView, ScheduleDetailView, SubmitAttendanceView,
                    ScheduleUpdateView, ScheduleDeleteView)


urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule'),
    path('check/', CheckAttendanceView.as_view(), name='check-attendance'),
    path('new/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('<int:pk>/submit/', SubmitAttendanceView.as_view(), name='submit-attendance'),
    path('<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
]
