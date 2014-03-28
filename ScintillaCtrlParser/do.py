funcprototype = """
OC_BEGIN_METHOD(%s, OCSyntaxEdit)
{
	CTRL_COMMON_HEADER(pWnd, pSAWnd, %d, %s, true);
	COCSyntaxEditCtrl* pEditCtrl = STATIC_DOWNCAST(COCSyntaxEditCtrl, pWnd);
	%s
	%s
}
OC_END_METHOD
"""

s = ''
with open("ScintillaCtrl.h") as fr:
    for line in fr:
        line = line.strip()

        brace = line.find('(')
        funcname = line[:brace]
        args = line[brace+1:-2].split(',')

        space = funcname.rfind(' ')

        ret = funcname[:space]
        funcname = funcname[space+1:]

        argparts = []
        argnames = []

        for idx, arg in enumerate(args):
            parts = arg.strip().split(' ')
            argtype = ' '.join(parts[:-1])
            argname = parts[-1]
            argnames.append(argname)

            if argtype == 'BOOL':
                argparts.append('OC_GET_BOOL(%d, %s)' % (idx, argname))
            elif argtype == 'int' or argtype == 'long':
                argparts.append('OC_GET_INT(%d, %s)' % (idx, argname))
            elif argtype == 'const char*':
                argparts.append('OC_GET_LPCSTR(%d, %s)' % (idx, argname))
            elif argtype == 'char*' or argtype == 'void*':
                argparts.append('OC_GET_LPSTR(%d, %s)' % (idx, argname))
            elif argtype == 'COLORREF' or argtype == 'DWORD':
                argparts.append('OC_GET_DWORD(%d, %s)' % (idx, argname))
            elif argtype == 'TextRange*':
                argparts.append('OC_GET_LPSTRUCT(%d, TextRange, %s)' % (idx, argname))
            elif argtype == 'TextToFind*':
                argparts.append('OC_GET_LPSTRUCT(%d, TextToFind, %s)' % (idx, argname))
            elif argtype == 'RangeToFormat*':
                argparts.append('OC_GET_LPSTRUCT(%d, RangeToFormat, %s)' % (idx, argname))

        retpart = ''
        if 'void' == ret:
            retpart = 'pEditCtrl->%s(%s);\n\treturn 0;' % (funcname, ','.join(argnames))
        else:
            ocfunc = ''
            if ret == 'BOOL' or ret == 'int' or ret == 'long' or ret == 'COLORREF':
                ocfunc = 'SetReturnInt'
            elif ret == 'CStringA':
                ocfunc = 'SetReturnString'
            elif ret == 'void*' or ret == 'const char*':
                ocfunc = 'SetReturnMemoryPtr'
            retpart = 'return pCall->%s(pEditCtrl->%s(%s));' % (ocfunc, funcname, ','.join(argnames))

        s += funcprototype % (funcname,
                len(args),
                'false' if ret == 'void' else 'true',
                '\n\t'.join(argparts),
                retpart
                )
        

with open("Out.cpp", "w") as fw:
    fw.write(s)

