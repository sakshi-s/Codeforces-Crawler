import requests
import pandas as pd
from .models import *
from . import fusioncharts
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()


def timetable(request):
    url = "https://codeforces.com/contests"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
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

    return render(request, 'cftimetable.html', {'contest_list' : contest_list})

def iitg(request):
    url = "https://codeforces.com/ratings/organization/297"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    num_pages_div = soup.find_all('div', class_ = 'pagination')

    if len(num_pages_div) == 1:
        num_pages = 1

    else:
        ul = num_pages_div[1].find('ul')
        li = ul.find_all('li')
        num_pages = int(li[-2].text)

    coders = []
    for i in range(num_pages + 1):
        url = "https://codeforces.com/ratings/organization/297/page/" + str(i+1)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        div = soup.find_all('div', class_ = 'datatable ratingsDatatable')
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
                if char == '(':
                    break
                if char >= '0' and char <= '9':
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
    if request.method == 'POST':
        handle = request.POST['handle']
        reqtype = request.POST['reqtype']
        
        if reqtype == "User Info":
            return redirect('cfsearch/' + handle)
        else:
            return redirect('contest/' + handle)

    else :
        return render(request, 'cfsearch.html')

def userprofile(request, handle):
    base_url = "https://www.codeforces.com/"
    contests_url = base_url + 'profile/' + handle
    page = requests.get(contests_url)
    soup = BeautifulSoup(page.content, 'lxml')
    info_div = soup.find('div', class_ = 'info')
    main_info = info_div.find('div', class_ = 'main-info')

    return render(request, 'userprofile.html', {'userinfo' : main_info.text})

def contest(request,handle):
    contest_stats = fetch_contest_stats(handle)
    charts = {
        "output_languages" :  display_languages_stats(handle).render(),
        "output_verdicts" :  display_verdicts_stats(handle).render(),
        "output_levels" :  display_levels_stats(handle).render()
    }
    contest_stats.update(charts)

    return render(request, 'contest_stats.html', contest_stats)

def fetch_contest_stats(handle):
    start_url = "https://www.codeforces.com/"
    contests_url = start_url + 'contests/with/' + handle
    page = requests.get(contests_url)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table', class_='tablesorter user-contests-table')
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    delta_rating = []
    rank_list = []

    for row in rows:
        elements = row.find_all('td')
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

def get_submission_stats(handle):
    Languages.objects.all().delete()
    Verdicts.objects.all().delete()
    Levels.objects.all().delete()

    url = "https://codeforces.com/submissions/" + handle
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    num_pages_div = soup.find_all('div', class_ = 'pagination')

    if len(num_pages_div) == 1:
        num_pages = 1

    else:
        ul = num_pages_div[1].find('ul')
        li = ul.find_all('li')
        num_pages = int(li[-2].text)

    language_series = pd.Series()
    verdict_series = pd.Series()
    level_series = pd.Series()

    for i in range(num_pages + 1):
        page = pd.read_html("https://codeforces.com/submissions/" + handle + "/page/" + str(i+1))
        table = page[0]

        language_series = language_series.combine(table['Lang'].value_counts(), (lambda x1, x2 : x1+x2), fill_value = 0)
        verdict_series = verdict_series.combine(table['Verdict'].value_counts(), (lambda x1, x2 : x1+x2), fill_value = 0)
        level_series = level_series.combine(table['Problem'].value_counts(), (lambda x1, x2 : x1+x2), fill_value = 0) 

    language_labels = language_series.keys()
    verdict_labels = verdict_series.keys()
    level_labels = level_series.keys()

    for label in language_labels:
        language = Languages.objects.update_or_create(name = label, val = language_series[label])[0]
        language.save()

    for label in verdict_labels:
        verdict = Verdicts.objects.update_or_create(name = label, val = verdict_series[label])[0]
        verdict.save()

    for label in level_labels:
        level = Levels.objects.update_or_create(name = label, val = level_series[label])[0]
        level.save()


def display_languages_stats(handle):
    # Saves stats data in database
    get_submission_stats(handle)

    chartConfig = dict()
    chartConfig["caption"] = "Languages of " + handle
    chartConfig["xAxisName"] = "Languages"
    chartConfig["xAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"

    datasource = dict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []
    
    for l in Languages.objects.all():
        datasource["data"].append({"label" : l.name, "value" : str(l.val)})

    graph2D = fusioncharts.FusionCharts("pie2d", "Languages Chart", "700", "500", "languages_chart", "json", datasource)

    return graph2D


def display_verdicts_stats(handle):
    chartConfig = dict()
    chartConfig["caption"] = "Verdicts of " + handle
    chartConfig["xAxisName"] = "Verdicts"
    chartConfig["xAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"

    datasource = dict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []

    WA = 0
    AC = 0
    RTE = 0
    MLE = 0
    CE = 0
    TLE = 0

    for verdict_object in Verdicts.objects.all():
        verdict = verdict_object.name
        if verdict[:5] == "Wrong":
            WA += verdict_object.val

        elif verdict[:5] == "Time":
            TLE += verdict_object.val

        elif verdict == "Accepted":
            AC += verdict_object.val

        elif verdict[:6] == "Memory":
            MLE += verdict_object.val

        elif verdict[:11] == "Compilation":
            CE += verdict_object.val

        elif verdict[:7] == "Runtime":
            RTE += verdict_object.val

    datasource["data"].append({"label" : "Accepted", "value" : AC})
    datasource["data"].append({"label" : "Wrong Answer", "value" : WA})
    datasource["data"].append({"label" : "Runtime Error", "value" : RTE})
    datasource["data"].append({"label" : "Memory Limit Exceeded", "value" : MLE})
    datasource["data"].append({"label" : "Compilation Error", "value" : CE})
    datasource["data"].append({"label" : "Time Limit Exceeded", "value" : TLE})

    graph2D = fusioncharts.FusionCharts("pie2d", "Verdicts Chart", "700", "500", "verdicts_chart", "json", datasource)

    return graph2D

def display_levels_stats(handle):

    chartConfig = dict()
    chartConfig["caption"] = "Levels of " + handle
    chartConfig["xAxisName"] = "Levels"
    chartConfig["xAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"

    datasource = dict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []

    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    R = 0

    for level_object in Levels.objects.all():
        level = level_object.name
        if level[0] == "A":
            A += level_object.val

        elif level[0] == "B":
            B += level_object.val

        elif level[0] == "C":
            C += level_object.val

        elif level[0] == "D":
            D += level_object.val

        elif level[0] == "E":
            E += level_object.val

        else:
            R += level_object.val

    datasource["data"].append({"label": "A", "value": A})
    datasource["data"].append({"label": "B", "value": B})
    datasource["data"].append({"label": "C", "value": C})
    datasource["data"].append({"label": "D", "value": D})
    datasource["data"].append({"label": "E", "value": E})
    datasource["data"].append({"label": "R", "value": R})

    graph2D = fusioncharts.FusionCharts("column2d", "Levels Chart", "700", "500", "levels_chart", "json", datasource)

    return graph2D

def allchat(request):
    alluser = User.objects.all()
    return render(request, 'allchat.html', {'alluser' : alluser})

def chatroom(request, userid1, userid2):
    userid1 = int(userid1)
    userid2 = int(userid2)
    sender = userid1

    if userid1 > userid2:
        userid1,userid2 = userid2,userid1

    user1_ = User.objects.get(pk = userid1)
    user2_ = User.objects.get(pk = userid2)

    try:
        chatroom = Chatroom.objects.get(user1=user1_, user2=user2_)

    except Chatroom.DoesNotExist:
        chatroom = Chatroom.objects.create(user1=user1_, user2=user2_)
        chatroom.save()

    if request.method == 'POST':
        message = request.POST['message']
        chatmessage = Chatmessage.objects.create(message = message, chatroom_id = chatroom.id, user_id = sender)
        chatmessage.save()
        return redirect('/')

    messages = Chatmessage.objects.filter(chatroom = chatroom)
    return render(request, 'chat.html', {'chatroom' : chatroom, 'messages' : messages})
    



