import os
import sys
from urllib.request import urlopen
import LTFuncsHTMLParser
import GenerateLTFuncHTML

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))


def generate_HTML(lang):
    def htmlfile(lang):
        return os.path.join(currentpath, 'Default%s.html' % lang)

    def httplink(lang):
        return 'http://wikis/ltwiki/index.php?title=Script%3ALabTalk-Supported_Functions-vNext'

    with urlopen(httplink(lang)) as r:
        parser = LTFuncsHTMLParser.MyHTMLParser()
        parser.feed(r.read().decode())

        # print('\n'.join(parser.results))
        generate = GenerateLTFuncHTML.GenerateHTML(lang, parser.results)

        with open(os.path.join(currentpath, "Default.html"), encoding='utf-8-sig') as fr:
            s = fr.read()
            gs = generate.Exec().replace('/images/docwiki/math', './images')
            s = s.replace('<div style="display: none" id="labtalkFunctions"></div>',
                          '<div style="display: none" id="labtalkFunctions">' + gs + '</div>')
            with open(htmlfile(lang), 'w', encoding='utf-8-sig') as fw:
                fw.write(s)

    return (True, "%s generated" % htmlfile(lang))


if __name__ == "__main__":
    result = generate_HTML(sys.argv[1])
    print(result[1])
