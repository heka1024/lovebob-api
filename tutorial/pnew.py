import requests
import re as regex
from bs4 import BeautifulSoup
import json


url = 'http://map.snu.ac.kr/api/amenities.action?convin_inst_knd_cd=4&current_lat_val=&current_lon_val='
response = requests.get(url)
data = response.json()

l = [[i['convin_inst_kor_nm'], i['lat_val'], i['lon_val']] for i in data['rows']]
for i in l:
    a, b = map(float, (i[1], i[2]))
    print(i[0], a, b)