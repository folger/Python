from html.parser import HTMLParser
import requests
import bs4

# url = 'http://wikis/ltwiki/index.php?title=Script%3ALabTalk-Supported_Functions'
# http_prefix = 'http://wikis'
# image_path = '/images/ltwiki/math/'
url = 'http://zaphod-w/doc/LabTalk/guide/LT-Supported-Functions'
http_prefix = 'http://zaphod-w'
image_path = r'/doc\{}/LabTalk/images/LabTalk-Supported_Functions/'


def get_url(lang):
    return url


def get_http_prefix(lang):
    return http_prefix


lang_map = {'E': 'en', 'J': 'ja', 'G': 'de'}


def get_image_path(lang):
    return image_path.format(lang_map[lang])


def get_page_source(lang):
    r = requests.get(get_url(lang))
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    hiddens = soup('input', type='hidden')

    data = {}
    for hidden in hiddens:
        data[hidden['name']] = hidden['value']
    data['ToolkitScriptManager1_HiddenField'] = 'ToolkitScriptManager1_HiddenField:;;AjaxControlToolkit, Version=3.5.50508.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:3656afa9-406a-4247-9088-5766fe2d8372:de1feab2:f9cec9bc:a67c2700:f2c8e708:720a52bf:589eaa30:698129cf:59fb9c6f'
    data['__EVENTTARGET'] = 'Header1$LanguageSwitch2'
    data['Header1$TextBoxSearch'] = 'Search'
    data['Header1$LanguageSwitch2'] = lang_map[lang]
    data['TheContentPage$ctl00$ctl00$TextBox_SearchInput'] = ''
    data['TheContentPage$ctl00$ctl00$DropDownList_Book'] = 'LabTalk'

    r = requests.post(url, data)
    return r.text


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()

        self.h2 = False
        self.h3 = False
        self.category = False
        self.subcategory = False
        self.lastcategory = ""

        self.table = False
        self.FitFunc = False

        self.col = 0
        self.a = False

        self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.h2 = True
        elif tag == "h3":
            self.h3 = True
        elif tag == "span":
            if attrs and attrs[0][0] == 'class' and attrs[0][1] == 'mw-headline':
                if self.h3:
                    self.subcategory = True
                elif self.h2:
                    self.category = True
        elif tag == "table":
            if attrs and attrs[0][0] == 'class' and (attrs[0][1] == 'simple-LTFunc' or attrs[0][1] == 'simple-FitFunc'):
                self.table = True
                self.FitFunc = attrs[0][1] == 'simple-FitFunc'

        if self.table:
            if tag == "tr":
                self.col = 0
                self.description = ''
            elif tag == "td":
                self.col += 1
            elif tag == "a":
                if self.col == 1:
                    self.a = True
                    for attr in attrs:
                        if attr[0] == 'href':
                            funclink = attr[1]
                            if not funclink.startswith('http://'):
                                funclink = 'http://www.originlab.com' + funclink
                            self.description += funclink
                            self.description += "\t" * 10
                            break
            else:
                if self.isFunction() or self.isDescription():
                    if len(attrs):
                        self.description += "<%s %s>" % (tag, ' '.join(['%s="%s"' % (key, value.replace("\n", "")) for (key, value) in attrs]))
                    else:
                        self.description += "<%s>" % tag

    def handle_endtag(self, tag):
        if tag == "h2":
            self.h2 = False
        elif tag == "h3":
            self.h3 = False
        elif tag == "span":
            self.category = False
            self.subcategory = False

        if self.table:
            if tag == "table":
                self.table = False

        if self.table:
            if tag == "td":
                if self.isDescription():
                    # print(self.description.strip())
                    description = self.description.strip()
                    if len(description) != 0:
                        self.results.append(self.polishDescription(description))
            elif tag == "a":
                if self.isFunction():
                    self.a = False
                    self.description += "\t" * 10
            else:
                if self.isFunction() or self.isDescription():
                    if tag != "br":
                        self.description += "</%s>" % tag

    def handle_data(self, data):
        if self.category:
            if data[0] == ' ' and self.lastcategory[-1] == ' ':
                self.lastcategory = self.lastcategory + '&' + data
                self.results[-1] = self.lastcategory
            else:
                self.lastcategory = data
                self.results.append(data)
        elif self.subcategory:
            if not self.results[-1].startswith("http"):
                del self.results[-1]
            self.results.append(self.lastcategory + " - " + data)
        elif self.isFunction() or self.isDescription():
            if self.isFunction() and self.FitFunc:
                self.description += "nlf_"
            self.description += data.replace("\n", "")

    def handle_entityref(self, ref):
        self.handle_data('&{};'.format(ref))

    def handle_charref(self, ref):
        self.handle_data('&#{};'.format(ref))

    def isFunction(self):
        return self.col == 1 and self.a

    def isDescription(self):
        return self.col == 2

    def polishDescription(self, description):
        for s, v, in (('<ul>', '<dl>'), ('</ul>', '</dl>'), ('<li>', '<dd>'), ('</li>', '</dd>'), ('&#160;', ' ')):
            description = description.replace(s, v)
        return description


if __name__ == "__main__":
    lang = 'E'
    parser = MyHTMLParser()
    parser.feed(get_page_source(lang))
    with open('parse_results_{}.txt'.format(lang), 'w', encoding='utf-8') as fw:
        for result in parser.results:
            print(result, file=fw)
