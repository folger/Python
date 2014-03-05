from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.table = False
        self.FitFunc = False

        self.col = 0
        self.a = False

        self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
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
          else:
            if self.isFunction() or self.isDescription():
              self.description += "<%s %s>" % (tag, ' '.join(['%s="%s"' % (key, value.replace("\n", "")) for (key, value) in attrs]))
        
    def handle_endtag(self, tag):
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
                    self.description += "</%s>" % tag
          
    def handle_data(self, data):
        if self.isFunction() or self.isDescription():
            if self.isFunction() and self.FitFunc:
                self.description += "nlf_"
            self.description += data.replace("\n", "")

    def isFunction(self):
        return self.col == 1 and self.a

    def isDescription(self):
        return self.col == 2


