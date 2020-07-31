import os
import sys
import requests
import re
from bs4 import BeautifulSoup
import shutil
import time
import MySQLdb
#import mysql.connector

def info_arr_extraction(row_data, index):
    info_arr = []
    #contest name
    m_0 =   row_data[0].text.strip()
    x = m_0.split("Enter")
    m_0 = x[0]
    #time
    # if index == 0:
    #     m_2 =  row_data[2].find('a').text.strip()
    # else:
    #     m_2 =  row_data[2].text.strip()
    m_2 =  row_data[2].text.strip()
    
    #"Length
    m_3 =  row_data[3].text.strip()
    m_0 = " ".join(m_0.split())
    m_2 = " ".join(m_2.split())
    m_3 = " ".join(m_3.split())
    if index==1:
    	m_2 = m_2[0:18]

    #converting to int
    #m_2 = int(m_2)
    #m_3 = int(m_3)

    info_arr.append(m_0)
    info_arr.append(m_2)
    info_arr.append(m_3)

    return info_arr


URL = "https://codeforces.com/contests?complete=true"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
contests = soup.find_all('div', attrs={"class": "datatable"})


info = []
for i in range(2):
	# if i == 0:
	#         continue
	body = contests[i].find('tbody')
	trs = body.find_all('tr')
	for j in range(len(trs)):
	    if j == 0:
	        continue
	    row = trs[j].find_all('td')
	    #print(trs[j]['data-contestid'])
	    info_arr = info_arr_extraction(row, i)
	    #"Contest id
	    m_4 =   trs[j]['data-contestid']
	    # m_4 = int(m_4)
	    info_arr.append(m_4)
	    info.append(info_arr)

print(*info, sep = "\n")
import csv

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(info)

# print(len(contests))
