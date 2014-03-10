import sys
from urllib.request import urlopen
import LTFuncsHTMLParser
import GenerateLTFuncHTML

def generate_HTML(lang):
    def htmlfile(lang):
        return 'Default%s.html' % lang

    def httplink(lang):
        return 'http://wikis/ltwiki/index.php?title=Script%3ALabTalk-Supported_Functions'

    with urlopen(httplink(lang)) as r:
        parser = LTFuncsHTMLParser.MyHTMLParser()
        parser.feed(r.read().decode())

        # print('\n'.join(parser.results))
        generate = GenerateLTFuncHTML.GenerateHTML(lang, parser.results)

        with open("Default.html", encoding='utf-8-sig') as fr:
            s = fr.read()
            gs = generate.Exec().replace('/images/docwiki/math', './images')
            s = s.replace('<div style="display: none" id="labtalkFunctions"></div>', '<div style="display: none" id="labtalkFunctions">' + gs + '</div>')
            with open(htmlfile(lang), 'w', encoding='utf-8-sig') as fw:
                fw.write(s)

    return (True, "%s generated" % htmlfile(lang))


if __name__ == "__main__":
    result = generate_HTML(sys.argv[1])
    print(result[1])