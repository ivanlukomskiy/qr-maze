import collections
import os
import re
import subprocess
import sys

import requests as requests

PREF = 'http://51.250.1.88'
START_PAGE = '/entrypoint.png'
TMP_IMG = 'tmp.png'

keys = {}

def parse(link):
    img_data = requests.get(link).content
    with open(TMP_IMG, 'wb') as handler:
        handler.write(img_data)

    res = subprocess.check_output(['zbarimg', 'tmp.png'])
    ress = res.decode("utf-8")
    try:
        resl = re.findall('(/\w+.png)', ress)
    except:
        print(f'res was {res}')
    if len(resl) == 0 and "Oh no, it' a dead end!" not in ress:
        k = re.findall('key \[(\d+)], it\'s "(\w+)"', ress)
        if len(k) == 1:
            # import ipdb; ipdb.set_trace()
            keys[k[0][0]] = k[0][1]
        else:
            print('Got something')
            print(res)
            sys.exit(1)
    return resl

i = 0
visited = set()
pending = collections.deque()
pending.append(START_PAGE)

while len(pending) > 0:
    addr = pending.pop()
    addresses = parse(PREF + addr)
    for address in addresses:
        if address not in visited:
            pending.append(address)
    print(f'{i}: {addr}')
    visited.add(addr)
    i += 1

for k, v in keys.items():
    print(f'{k} -> {v}')
