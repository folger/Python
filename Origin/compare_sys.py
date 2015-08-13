import os
import requests
import bs4


okSysValues = os.path.join(os.environ['Develop'],
                           r'Source\vc32\okern96\okSysValues.cpp')
with open(okSysValues) as f:
    data = f.read()


def from_web():
    res = requests.get('http://www.originlab.com/doc/LabTalk/ref/sys-var-list')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    for table in soup(class_='simple'):
        tbody = table.tbody
        if not tbody:
            tbody = table
        for tr in tbody.children:
            if not isinstance(tr, bs4.element.Tag):
                continue
            td = tr.td
            if td:
                yield td.text.strip()[1:]


def from_file():
    with open(r'F:\vars.txt') as f:
        for line in f:
            yield line.rstrip()

for name in from_file():
    if (data.find('(' + name + ',') < 0 and
       data.find('(' + name + ')') < 0):
        print(name)
os.system('pause')
