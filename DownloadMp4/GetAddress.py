from selenium import webdriver
import re
from time import sleep

driver = webdriver.Chrome(r'c:\box\Windows\chromedriver.exe')
preSrc = re.compile("(http://tv.sohuxia.com/\d+/n\d+\.shtml)' >第(\d+)集")
preDes = re.compile('http://\d+\.\d+\.\d+\.\d+[^"]+')

block = 5
outfile = "Shield.txt"

with open(outfile, "w") as fw:
    with open("Addrs.txt", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            m = preSrc.search(line)
            if m:
                print(m.group(2))
                fw.write(m.group(2) + '\n')

                driver.get(m.group(1))
                sleep(3)

                all = preDes.findall(driver.page_source)
                fw.write('\n'.join(all[block:2*block]) + '\n')
                





