from django.shortcuts import render
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
    url1 = "https://codeforces.com/ratings/organization/297"
    page1 = requests.get(url1)
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    div1 = soup1.find_all('div', class_='pagination')

    if len(div1) == 1:
        t = 1
    else:
        ul = div1[1].find('ul')
        li = ul.find_all('li')

        t = int(li[-2].text)

    dic = []
    for i in range(t + 1):
        url = "https://codeforces.com/ratings/organization/297/page/" + str(i+1)
        # print(url)
        page = requests.get(url)
        bs = BeautifulSoup(page.content, 'html.parser')
        div = bs.find_all('div',class_='datatable ratingsDatatable')
        # print(div)
        tables = div[0].find_all('table')

        sec=tables[0].find_all('tr')
        for item in sec:
            secx = item.find_all('td')

            if len(secx) == 0:
                continue
            list = []
            stri = secx[0].text.strip()
            r = 0
            for e in stri:
                if e =='(':
                    break
                if e>='0' and e<='9':
                    r = r*10 + int(e)
            if r==0:
                continue
            list.append(r)
            list.append(secx[1].text.strip())
            list.append(sec[1].find_all('a')[0]['class'][1])
            list.append(secx[2].text.strip())
            list.append(secx[3].text.strip())
            dic.append(list)
    print(dic)
    return render(request, 'iitg.html', {'dic':dic})
