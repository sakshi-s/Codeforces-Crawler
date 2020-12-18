import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    return render(request, 'home.html')

def timetable(request):
    return render(request, 'timetable.html')

def iitg(request, bakchodi):
    return render(request, 'iitg.html')

def search(request):
    return render(request, 'searchhandle.html')

def allchat(request):
    alluser = User.objects.all()
    return render(request, 'allchat.html', {'alluser': alluser})