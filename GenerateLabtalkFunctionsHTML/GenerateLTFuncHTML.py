import os
import re
from xml.etree import ElementTree as ET

import LTFuncsHTMLParser


class HTMLType:
    ALL, SCV, FO, NLFIT = range(4)


def _func_entries(funcs):
    for func in funcs:
        yield func.split("\t" * 10)


class GenerateHTML:
    def __init__(self, lang, funcs):
        self.funcs = funcs
        self.lang = lang

    def Exec(self, htmlType):
        s = ''

        fitfunc = False
        funcs_done = set()
        fitfunc_categoryname = ''

        def check_htmlType_continue():
            if fitfunc:
                if htmlType == HTMLType.NLFIT and fitfunc_categoryname in ('Implicit', 'PFW', 'Surface Fitting'):
                    return True
                if htmlType == HTMLType.SCV and fitfunc_categoryname in ('Multiple Variables',):
                    return True
            else:
                if htmlType == HTMLType.FO or htmlType == HTMLType.NLFIT:
                    return True
            return False

        fitting_function_prefixs = {'E': 'Fitting Functions', 'J': 'フィット関数', 'G': 'Fitting Functions'}
        for entries in _func_entries(self.funcs):
            if len(entries) == 1:  # category
                func = entries[0]
                funcs_done.clear()
                fitfunc = func.startswith(fitting_function_prefixs[self.lang])
                if fitfunc:
                    fitfunc_categoryname = func.split('-')[1].lstrip()
                    if htmlType != HTMLType.SCV:
                        func = fitfunc_categoryname
                if check_htmlType_continue():
                    continue
                if len(s):
                    s += '</table>\n'
                s += '<table>\n    <caption>%s</caption>\n' % func.strip()
            else:
                if check_htmlType_continue():
                    continue
                total = (len(entries) - 1) // 2
                for i in range(total):
                    funclink = entries[i * 2].strip()
                    funcname = entries[i * 2 + 1].strip()
                    description = entries[-1].strip()
                    funcnametest = funcname
                    if fitfunc:
                        funcnametest = 'nlf_' + funcnametest
                    if funcnametest in funcs_done:
                        continue
                    funcs_done.add(funcnametest)
                    if not funclink.startswith('http'):
                        funclink = 'http://wikis' + funclink
                    s += '    <tr>\n        <td><a href="%s" fprefix="%s">%s</a></td>\n        <td>%s</td>\n    </tr>\n' \
                        % (funclink, "nlf_" if fitfunc else "", funcname[len("nlf_"):] if fitfunc else funcname, description)

        if len(s):
            s += '</table>'
        s = s.replace(LTFuncsHTMLParser.get_image_path(self.lang), './images/')
        return s


class GenerateXML:
    def __init__(self):
        self.lang = 'E'
        parser = LTFuncsHTMLParser.MyHTMLParser()
        parser.feed(LTFuncsHTMLParser.get_page_source(self.lang))
        self.funcs = parser.results
        # with open('parse_results_{}.txt'.format(self.lang), encoding='utf-8') as f:
            # self.funcs = f.readlines()

    def Exec(self):
        imagepath = LTFuncsHTMLParser.get_image_path(self.lang).replace('\\', '\\\\')
        p_imagepath = re.compile(r'src="({}.+?\.png)"'.format(imagepath))
        root = ET.Element('Root')
        tree = ET.ElementTree(root)
        for entries in _func_entries(self.funcs):
            if len(entries) == 1:  # category
                category = ET.SubElement(root, 'Category')
                category.set('Label', entries[0])
            else:
                func = entries[1]
                function = ET.SubElement(category, func[:func.find('(')])
                function.text = func
                images = p_imagepath.findall(entries[2])
                if images:
                    function.set('images', '|'.join(images))

        with open('Functions.xml', 'w', encoding='utf-8') as f:
            tree.write(f, encoding='unicode')
