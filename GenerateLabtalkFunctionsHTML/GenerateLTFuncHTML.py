class HTMLType:
    ALL, SCV, FO, NLFIT = range(4)


class GenerateHTML:
    def __init__(self, lang, funcs):
        self.funcs = funcs

        self.lang = lang.upper()

    def Exec(self, htmlType):
        s = ''

        fitfunc = False
        funcs_done = set()
        fitfunc_categoryname = ''

        def check_htmlType_continue():
            if fitfunc:
                if htmlType == HTMLType.NLFIT and fitfunc_categoryname in ('Implicit', 'PFW', 'Surface Fitting'):
                    return True
            else:
                if htmlType == HTMLType.FO or htmlType == HTMLType.NLFIT:
                    return True
            return False

        for func in self.funcs:
            entries = func.split("\t"*10)
            if len(entries) == 1:  # category
                funcs_done.clear()
                fitfunc = func.startswith('Fitting Functions')
                if fitfunc:
                    if htmlType == HTMLType.FO or htmlType == HTMLType.NLFIT:
                        fitfunc_categoryname = func.split('-')[1].lstrip()
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
                    funclink = entries[i*2].strip()
                    funcname = entries[i*2+1].strip()
                    description = entries[-1].strip()
                    funcnamenoargs = funcname.split('(')[0].lower()
                    if fitfunc:
                        funcnamenoargs = 'nlf_' + funcnamenoargs
                    if funcnamenoargs in funcs_done:
                        continue
                    funcs_done.add(funcnamenoargs)
                    if not funclink.startswith('http://'):
                        funclink = 'http://wikis' + funclink
                    s += '    <tr>\n        <td><a href="%s" fprefix="%s">%s</a></td>\n        <td>%s</td>\n    </tr>\n' \
                        % (funclink, "nlf_" if fitfunc else "", funcname[len("nlf_"):] if fitfunc else funcname, description)

        if len(s):
            s += '</table>'
        s = s.replace('/images/ltwiki/math/', './images/')
        return s
