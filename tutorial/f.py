import requests
import re as regex
import sys
from bs4 import BeautifulSoup
from datetime import date

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")

import django
django.setup()

from quickstart.models import *

def get_pos():
    x = '''
37.45932 126.95058
37.45647 126.94851
37.46306 126.95872
37.44887 126.95265
37.46504 126.95175
37.46098 126.95252
37.46073 126.9557
37.45016 126.95259
37.46193 126.95312
37.4592190840394 126.94812006718699
37.45727 126.95079
37.46504 126.95175
37.46451 126.95424
37.46504 126.95175
37.46328 126.95015
'''
    l = [[float(a), float(b)] for (a, b) in [i.split(' ') for i in x.split('\n') if i != '']]
    return l

url = 'http://snuco.snu.ac.kr/ko/node/20'
sel = '#node-20 > div > div > div > div > table > tbody > tr'
html = BeautifulSoup(requests.get(url).text, 'html.parser')
l = [[i.text.replace('\n', '').replace('\t', '') for i in c.children if i != '\n'] for c in html.select(sel)]
ll = [i for i in l if len(i) != 6 and len(i) != 5]
pat = regex.compile(r'(.+)\((\d+-\d+)\)')
loc = get_pos()
for idx, (i, j) in enumerate(zip(ll, loc)):
    location = i[1]
    name, n = pat.findall(i[0])[0]
    lat, lng = j
    print(idx, name, n, location, lat, lng)
    # pnew = Restaurant(
    #     name = name,
    #     number = '02-' + n,
    #     location = location,
    #     lng = lng, lat = lat,
    #     id = idx
    # )
    # pnew.save()
    # print(pnew)