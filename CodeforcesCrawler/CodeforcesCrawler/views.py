import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def timetable(request):
    return render(request, 'timetable.html')

def iitg(request, bakchodi):
    return render(request, 'iitg.html')

def search(request):
    return render(request, 'searchhandle.html')

def userprofile(request, handle):
    base_url = "https://www.codeforces.com/"
    contests_url = base_url + 'profile/' + handle
    page = requests.get(contests_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info_div = soup.find('div', class_='info')
    main_info = info_div.find('div', class_='main-info')
    return render(request, 'userprofile.html', {'userinfo' : main_info.text})