import re
import sys

def repl(match):
    s = match.group(1)
    return '<a href="mailto:{}">{}</a>'.format(s, s)

if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        s = f.read()
        s = re.sub('&', '&amp;', s)
        s = re.sub('<', '&lt', s)
        s = re.sub('>', '&gt', s)

        s = re.sub('^\s*$', '<p>', s)

        hostNameRegEx = r'[-a-z0-9]+(\.[-a-z0-9]+)*\.(com|edu|info)'
        #replace email address
        s = re.sub(r'''
                \b
                (
                    \w[-.\w]*
                    @
                    {}
                )
                \b
'''.format(hostNameRegEx), repl, s, 0, re.I | re.X)

        #replace URL
        s = re.sub(r'''
                \b
                (
                    http:// {} \b
                    (
                        / [-a-z0-9_:\@&?=+,.!/~*%\$]*
                        (?<![.,?!])
                    )?
                )
'''.format(hostNameRegEx), repl, s, 0, re.I | re.X)

        print(s)
