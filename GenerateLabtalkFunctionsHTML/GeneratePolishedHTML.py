import os
import sys
from urllib.request import urlopen
import LTFuncsHTMLParser
from GenerateLTFuncHTML import GenerateHTML, HTMLType

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))


def generate_HTML(lang, htmlType):
    def htmlfile():
        if htmlType == HTMLType.SCV:
            return os.path.join(currentpath, 'SCV_%s.html' % lang)
        if htmlType == HTMLType.FO:
            return os.path.join(currentpath, 'FO_%s.html' % lang)
        if htmlType == HTMLType.NLFIT:
            return os.path.join(currentpath, 'NLFIT_%s.html' % lang)
        return os.path.join(currentpath, 'ALL_%s.html' % lang)

    def basicHTML():
        htmls = {
            'E': 'Default.html',
            'G': 'DefaultG.html',
            'J': 'DefaultJ.html',
        }
        return htmls[lang]

    parser = LTFuncsHTMLParser.MyHTMLParser()
    parser.feed(LTFuncsHTMLParser.get_page_source(lang))

    # print('\n'.join(parser.results))
    generate = GenerateHTML(lang, parser.results)

    with open(os.path.join(currentpath, basicHTML()), encoding='utf-8-sig') as fr:
        s = fr.read()
        if htmlType == HTMLType.FO or htmlType == HTMLType.NLFIT:
            s = s.replace('navigate("//select:" + ui.item.fprefix + ui.item.label);', 'navigate("//select:" + ui.item.category + "|" + ui.item.label);')
        gs = generate.Exec(htmlType).replace('/images/docwiki/math', './images')
        s = s.replace('<div style="display: none" id="labtalkFunctions"></div>',
                      '<div style="display: none" id="labtalkFunctions">' + gs + '</div>')
        with open(htmlfile(), 'w', encoding='utf-8-sig') as fw:
            fw.write(s)

    return (True, "%s generated" % htmlfile())


if __name__ == "__main__":
    result = generate_HTML(sys.argv[1])
    print(result[1])
