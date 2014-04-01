class GenerateHTML:
    def __init__(self, lang, funcs):
        self.funcs = funcs

        self.lang = lang.upper()
        self.funcs_descriptions = {}
        for func in funcs:
            entries = func.split('\t'*10)
            description = entries[-1]
            for entry in entries[:-1]:
                self.funcs_descriptions[entry.split('(')[0].lower()] = (entry, description)

    def Exec(self):
        s = ''

        fitfunc = False
        funcs_done = set()

        for func in self.funcs:
            entries = func.split("\t"*10)
            if len(entries) == 1:  # categoty
                funcs_done.clear()
                fitfunc = func.startswith('Fitting Functions')
                if len(s):
                    s += '</table>\n'
                s += '<table>\n    <caption>%s</caption>\n' % func.strip()
            else:
                funcname = entries[0].strip()
                description = entries[1].strip()
                funcnamenoargs = funcname.split('(')[0].lower()
                if fitfunc:
                    funcnamenoargs = 'nlf_' + funcnamenoargs
                if funcnamenoargs in funcs_done:
                    continue
                funcs_done.add(funcnamenoargs)
                s += '    <tr>\n        <td><a href="/junk">%s</a></td>\n        <td>%s</td>\n    </tr>\n' \
                    % (funcname[len("nlf_"):] if fitfunc else funcname, description)

        if len(s):
            s += '</table>'
        s = s.replace('/images/ltwiki/math/', './images/')
        return s
