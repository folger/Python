class GenerateHTML:
    def __init__(self, lang, funcs):
        self.lang = lang.upper()
        self.funcs_descriptions = {}
        for func in funcs:
            entries = func.split('\t'*10)
            description = entries[-1]
            for entry in entries[:-1]:
                self.funcs_descriptions[entry.split('(')[0].lower()] = (entry, description)

    def Exec(self):
        with open(r'SCVFuncs.txt') as f:
            s = ''
            fcate = open(r'Category%s.txt' % self.lang, encoding='utf-8-sig') if self.lang != 'E' else None
            categorys = {}
            if fcate:
                for line in fcate:
                    if len(line):
                        entries = line.split('\t')
                        categorys[entries[0]] = entries[1]

            fitfunc = False
            funcs_done = set()
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                if line.endswith('$') or line.endswith(')'): # function
                    try:
                        functionname = line.split('(')[0].lower()
                        if fitfunc:
                            functionname = 'nlf_' + functionname
                        if functionname in funcs_done:
                            continue
                        funcs_done.add(functionname)
                        funcs_description = self.funcs_descriptions[functionname]
                        s += '    <tr>\n        <td><a href="/junk">%s</a></td>\n        <td>%s</td>\n    </tr>\n' % (funcs_description[0][4:] if fitfunc else funcs_description[0], funcs_description[1].strip())
                    except KeyError as e:
                        pass
                        # print("Missing function: %s" % line)
                else: # category
                    funcs_done.clear()
                    fitfunc = line.startswith('Fitting Functions')
                    if len(s):
                        s += '</table>\n'
                    if len(categorys):
                        try:
                            line = categorys[line]
                        except KeyError:
                            print("Category %s not found in Category%s.txt !!!" % (line, self.lang))

                    s += '<table>\n    <caption>%s</caption>\n' % line.strip()
            if len(s):
                s += '</table>'
            s = s.replace('/images/ltwiki/math/', './images/')
            return s




