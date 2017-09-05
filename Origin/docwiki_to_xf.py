import requests
import bs4


r = requests.get('http://wikis/wiki2/index.php?title=X-Function%3AWcellfmt-vNext', timeout=30)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

brief_information_node = soup(id='Brief_Information')[0].parent.next_sibling
while True:
    try:
        brief_information = brief_information_node.text.strip()
        break
    except:
        brief_information_node = brief_information_node.next_sibling
print(brief_information)
