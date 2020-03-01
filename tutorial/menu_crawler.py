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

def getUrl(s):
    y, m, d = s.split('-')
    base = 'http://snuco.snu.ac.kr/foodmenu' \
        + '?field_menu_date_value_1%5Bvalue%5D%5Bdate%5D=&field_menu_date_value%5Bvalue%5D%5B' \
        +  f'date%5D={m}%2F{d}%2F{y}'
    return base

def nameAndNumber(s):
    p = regex.compile(r'(.+)\((\d+-\d+)\)')
    tmp = p.findall(s)
    if tmp == []:
        return None
    else:
        name, n = tmp[0]
        n = f'02-{n}'
        return name, n
    
def menu2dict(menu):
    p = regex.compile(r'(.+) (\d+,\d+)')
    tmp = p.findall(menu)
    if tmp == []:
        return {'name': '', 'price': -1}
    else:
        name, price_str = p.findall(menu)[0]
        price = int(price_str.replace(',', ''))
        return {'name': name, 'price': price}
    
def foodlist(l):
    ret = []
    for s in l:
        menu_str = (s.replace('\xa0', '')
                    .replace('(#)', '')
                    .replace('\n', '')
                    .replace('<301푸드코트>', '')
                    .replace('<교직', '')
                    .replace('식당>', ''))
        ret.append(
            menu2dict(menu_str)
        )
    return ret

def getDietOfDay(date = date.today().isoformat()):
    url = getUrl(date)
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    selector = '#main-content > div.contentsArea > div > div > div.view-content > table > tbody > tr'
    selected = soup.select(selector)
    
    for s in selected:
        # .views-field.views-field-field-restaurant
        k = ['breakfast', 'lunch', 'dinner']
        d = {}
        for i, c in enumerate(s.select(selector + '> td')):
            if i == 0:
                # d['name'] = c.text.strip()
                name, number = nameAndNumber(c.text.strip())
                d['name'] = name
                d['number'] = number
            else:                
                d[k[i-1]] = foodlist(c.text.strip().split('원')[:-1])
        yield d

def insert_db(menu_date):
    print("date is ", menu_date)
    for i in getDietOfDay(menu_date):
        restaurant_name = i['name']
        restaurant_number = i['number']

        for k in ('breakfast', 'lunch', 'dinner'):
            menus = i[k]
            for menu in menus:
                menu_name = menu['name']
                menu_price = menu['price']
                if '채식' in menu_name:
                    menu_name = '(채식) 채식뷔페'
                if '<주문식 코너>' in menu_name:
                    idx = menu_name.find('<주문식 코너>') + len('<주문식 코너>')
                    menu_name = menu_name[idx:].strip()
                
                if menu_price != -1:
                    print(restaurant_number)
                    r = Restaurant.objects.get(number = restaurant_number)
                    Menu(
                        name = menu_name,
                        price = menu_price,
                        date = menu_date,
                        restaurant = r,
                        time = k[0]
                    ).save()

if __name__ == "__main__":
    date = input("input date > ")
    insert_db(date)
	# insert_db(date)
