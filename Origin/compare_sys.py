import bs4
import os
import re
from datetime import datetime


okSysValues = os.path.join(os.environ['Develop'],
                           r'Source\vc32\okern96\okSysValues.cpp')
with open(okSysValues) as f:
    data = f.read()

with open(os.path.expanduser('~/Desktop/System Variable List.html'), encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f, 'html.parser')
    for table in soup(class_='simple'):
        for tr in table.tbody.children:
            if not isinstance(tr, bs4.element.Tag):
                continue
            td = tr.td
            if td:
                name = td.text.strip()[1:]
                if data.find('(' + name + ',') < 0 and data.find('(' + name + ')') < 0:
                    print(name)
