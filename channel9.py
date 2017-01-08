import os

import requests
import bs4

note = 'channel9.txt'
f = open(note, 'w')
for i in range(1, 10):
    url = 'https://channel9.msdn.com/series/GetStartedPowerShell3/{:02d}'.format(i)
    print(url)
    while True:
        try:
            r = requests.get(url, timeout=5)
            break
        except Exception:
            print('Fail, retry ...')
    bsoup = bs4.BeautifulSoup(r.text, 'html.parser')

    def get_link(fmt):
        return bsoup(attrs={'data-filename': fmt.format(i)})[0]['value']
    print(get_link('{:02d}_mid.mp4'), file=f)
    print(get_link('{:02d}_en.vtt'), file=f)
f.close()
os.system('start notepad {}'.format(note))
