import os
import re
import subprocess

import requests as requests

PREF = 'http://51.250.1.88'
START_PAGE = '/entrypoint.png'
TMP_IMG = 'tmp.png'

def parse(link):
    img_data = requests.get(link).content
    with open(TMP_IMG, 'wb') as handler:
        handler.write(img_data)

    res = subprocess.check_output(['zbarimg', 'tmp.png'])
    try:
        res = re.findall('(/\w+.png)', res.decode("utf-8"))
    except:
        print(f'res was {res}')
    return res

i = 0
addr = START_PAGE
visited = set()

while True:
    addresses = parse(PREF + addr)
    addr = addresses[0]
    print(f'{i}: {addr}')
    i += 1
