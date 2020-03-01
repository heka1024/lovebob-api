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

date = input('input date > ')
url = f'http://mini.snu.kr/cafe/set/{date}'
q = '#main > table'

req = requests.get(url)
req.encoding='utf-8'
html = BeautifulSoup(req.text, 'html.parser')
rows = html.select(q)[0].select('table > tr')

cnt = -1
cases = {0: [], 1: [], 2: []}
for s in rows:
    if len(s) == 1:
        cnt = cnt + 1
    else:
        cases[cnt] += [s]
        
if len(html.select(q)) > 1:
    for s in html.select(q)[1].select('table > tr'):
        cases[1] += [s]
        cases[2] += [s]

menus = []
for k, v in cases.items():
    for row in v:
        res_name, _, ms = row
        for td in row:
            for i, m in enumerate(ms):
                if m.name == 'span':
                    if m['class'][0] == 'price':
                        name = list(ms)[i+1]
                        price = int(m.text) * 100
                        menus += [{
                            'time': k,
                            'restaurant': res_name.text,
                            'name': name,
                            'price': price
                        }]

table = ['b', 'l', 'd']
for m in menus:
    r = Restaurant.objects.get(name = m['restaurant'])
    pnew = Menu(
        name = m['name'],
        price = m['price'],
        date = date,
        restaurant = r,
        time = table[m['time']]
    )
    print(pnew)
    pnew.save()
