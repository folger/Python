from selenium import webdriver
import re
from time import sleep

def OutputAddrs(preSrc, preDes, polishAddress):
    driver = webdriver.Chrome(r'c:\box\Windows\chromedriver.exe')
    
    with open("Now.txt", "w") as fw:
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
                    # ss = '\n'.join(all[block:2*block]) + '\n'
                    fw.write(polishAddress(all))

                





