from html.parser import HTMLParser


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
            if attrs and attrs[0][0] == 'class' and (attrs[0][1] == 'simple LTFunc' or attrs[0][1] == 'simple FitFunc'):
                self.table = True
                self.FitFunc = attrs[0][1] == 'simple FitFunc'

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
                                funclink = 'http://wikis' + funclink
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
                        self.results.append(description)
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
            if self.results[-1].find("-") == -1:
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

from urllib.request import urlopen

if __name__ == "__main__":
    with urlopen('http://wikis/ltwiki/index.php?title=Script%3ALabTalk-Supported_Functions-vNext') as r:
        parser = MyHTMLParser()
        parser.feed(r.read().decode())
        with open('parse_results.txt', 'w', encoding='utf-8') as fw:
            for result in parser.results:
                print(result, file=fw)
