import os
import re
import subprocess

import requests as requests

START_PAGE = 'http://51.250.1.88/entrypoint.png'
TMP_IMG = 'tmp.png'

def parse(link):
    img_data = requests.get(link).content
    with open(TMP_IMG, 'wb') as handler:
        handler.write(img_data)

    res = subprocess.check_output(['zbarimg', 'tmp.png'])
    res = re.findall('QR-Code:(.*)\\n', res.decode("utf-8"))[0]
    return res

addr = START_PAGE
while True:
    addr = parse(addr)
    print(addr)
