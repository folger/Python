from html.parser import HTMLParser
from urllib.request import urlopen

class MyHTMLParser(HTMLParser):
    def __init__(self):
      super(MyHTMLParser, self).__init__()
      self.table = False

      self.col = 0
      self.a = False

      self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
          if attrs and attrs[0][0] == 'class' and attrs[0][1] == 'simple LTFunc':
            self.table = True

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
              self.description += "<%s %s>" % (tag, ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs]))
        
    def handle_endtag(self, tag):
        if self.table:
          if tag == "table":
            self.table = False

          if self.table:
            if tag == "td":
              if self.isDescription():
                # print(self.description.strip())
                self.results.append(self.description.strip())
            elif tag == "a":
              if self.isFunction():
                self.a = False
                self.description += "\t" * 10
            else:
              if self.isFunction() or self.isDescription():
                self.description += "</%s>" % tag
          
    def handle_data(self, data):
        if self.isFunction() or self.isDescription():
          self.description += data

    def isFunction(self):
      return self.col == 1 and self.a

    def isDescription(self):
      return self.col == 2

        
#with open(r'd:\aaa\Script\LabTalk-Supported_Functions.html') as f:
with urlopen("http://wikis/ltwiki/index.php?title=Script:LabTalk-Supported_Functions") as r:
  # print(f.read().decode())
  parser = MyHTMLParser()
  parser.feed(r.read().decode())
  with open(r'g:\CheckCode\Python\SCVHtml\LTFuncs.txt', 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(parser.results))


