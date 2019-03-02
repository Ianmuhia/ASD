"""AttendanceSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from user import views as userViews
from home import views as homeViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', userViews.register, name='register'),
    path('', authViews.LoginView.as_view(template_name='user/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', authViews.LogoutView.as_view(), name='logout'),
    path('home/', homeViews.HomeView.as_view(), name='home'),
    path('subject/', include('subject.urls')),
    path('course/', include('course.urls')),
    path('student/', include('student.urls')),
    path('schedule/', include('schedule.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
