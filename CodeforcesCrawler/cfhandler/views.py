from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
import re
from urllib.request import urlopen
from django.views.generic import TemplateView
from . import fusioncharts
import pandas as pd
from matplotlib import pyplot as plt
from .models import *
from collections import OrderedDict
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def timetable(request):
    url = "https://codeforces.com/contests"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', class_="")
    contest_list = []

    rows = tables[0].find_all('tr')
    for row in rows:
        elements = row.find_all('td')
        elements = [element.text.strip() for element in elements]

        if len(elements) > 0:
            if elements[1] == '':
                elements[1] = "Not Mentioned"
            contest_list.append(elements)


    return render(request, 'cftimetable.html', {'contest_list': contest_list})

def iitg(request):
    url = "https://codeforces.com/ratings/organization/297"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    num_pages_div = soup.find_all('div', class_='pagination')

    if len(num_pages_div) == 1:
        num_pages = 1
    else:
        ul = num_pages_div[1].find('ul')
        li = ul.find_all('li')
        num_pages = int(li[-2].text)

    coders = []
    i = 1
    for i in range(num_pages + 1):
        url = "https://codeforces.com/ratings/organization/297/page/" + str(i+1)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all('div',class_='datatable ratingsDatatable')
        tables = div[0].find_all('table')

        rows = tables[0].find_all('tr')
        for row in rows:
            elements = row.find_all('td')

            if len(elements) == 0:
                continue
            coder_info = []
            column_text = elements[0].text.strip()
            rating = 0
            for char in column_text:
                if char =='(':
                    break
                if char>='0' and char<='9':
                    rating = rating*10 + int(char)
            if rating == 0:
                continue
            coder_info.append(rating)
            coder_info.append(elements[1].text.strip())
            coder_info.append(rows[1].find_all('a')[0]['class'][1])
            coder_info.append(elements[2].text.strip())
            coder_info.append(elements[3].text.strip())
            coders.append(coder_info)
    return render(request, 'cfiitg.html', {'coders':coders})

def cfsearch(request):
    if( request.method == 'POST') :
        handle = request.POST['handle']
        reqtype = request.POST['reqtype']
        
        if(reqtype == "User Info"):
            return redirect('cfsearch/' + handle)
        else:
            return redirect('contest/' + handle)

    else :
        return render(request, 'cfsearch.html')

def userprofile(request, handle):
    base_url = "https://www.codeforces.com/"
    contests_url = base_url + 'profile/' + handle
    page = requests.get(contests_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info_div = soup.find('div', class_='info')
    main_info = info_div.find('div', class_='main-info')
    return render(request, 'userprofile.html', {'userinfo' : main_info.text})

def contest(request,handle):
    fcs = fetch_contest_stats(handle)
    # chart = {"output_languages" :  display_stats_languages(handle).render()
    # }
    # fcs.update(chart)

    return render(request, 'contest_stats.html', fcs)

def fetch_contest_stats(handle):
    start_url = "https://www.codeforces.com/"

    contests_url = start_url + 'contests/with/' + handle
    page = requests.get(contests_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', class_='tablesorter user-contests-table')
    tbody = table.find('tbody')

    rows = tbody.find_all('tr')

    delta_rating = []
    rank_list = []

    for item in rows:
        elements = item.find_all('td')
        rank = int(elements[3].find('a').text)
        rating_change = int(elements[5].text)

        delta_rating.append(rating_change)
        rank_list.append(rank)

    delta_rating.sort()
    rank_list.sort()

    stats = {
        'Handle' : handle,
        'No_of_Contests' : rows[0].find('td').text,
        'Best_Rank' : rank_list[0],
        'Worst_Rank' : rank_list[len(rank_list)-1],
        'Max_Up' : delta_rating[len(delta_rating)-1],
        'Max_Down' : delta_rating[0],
    }

    return stats

