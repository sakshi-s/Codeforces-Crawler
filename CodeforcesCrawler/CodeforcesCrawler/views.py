from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def timetable(request):
    return render(request, 'timetable.html')

def iitg(request):
    return render(request, 'iitg.html')