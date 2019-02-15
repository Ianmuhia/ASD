from django.shortcuts import render


def logIn(request):
    return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/regsiter.html')
