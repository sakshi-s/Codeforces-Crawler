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
