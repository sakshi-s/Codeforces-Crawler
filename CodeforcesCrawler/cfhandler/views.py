from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup

# Create your views here.
def timetable(request):
    url = "https://codeforces.com/contests"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', class_="")
    contest_list = []

    rows = tables[0].find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        columns = [column.text.strip() for column in columns]

        if len(columns) > 0:
            if columns[1] == '':
                columns[1] = "Not Mentioned"
            contest_list.append(columns)


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
            columns = row.find_all('td')

            if len(columns) == 0:
                continue
            coder_info = []
            column_text = columns[0].text.strip()
            rating = 0
            for char in column_text:
                if char =='(':
                    break
                if char>='0' and char<='9':
                    rating = rating*10 + int(char)
            if rating == 0:
                continue
            coder_info.append(rating)
            coder_info.append(columns[1].text.strip())
            coder_info.append(rows[1].find_all('a')[0]['class'][1])
            coder_info.append(columns[2].text.strip())
            coder_info.append(columns[3].text.strip())
            coders.append(coder_info)
    return render(request, 'cfiitg.html', {'coders':coders})

def cfsearch(request):
    if( request.method == 'POST') :
        handle = request.POST['handle']
        reqtype = request.POST['reqtype']
        
        if(reqtype == "User Handle"):
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
    return redirect('/')

