import os
import re


codes = {
            'z': 'SVE({_name})',
            'ia': 'SVE_INT_ACCESS({_name}, _fn)',
            'r': 'SVE_READONLY({_name}, [](){return;})',
            'g': 'SVE_GENERAL({_name}, [](){return;}, [](double val){;})',
            'sb': 'SVE_SUB({_name}, _fn, _sub)',
            'c': 'SVE_CHAR({_name}, _default)',
            'by': 'SVE_BYTE({_name}, _default)',
            's': 'SVE_SHORT({_name}, _default)',
            'u': 'SVE_USHORT({_name}, _default)',
            'dw': 'SVE_DWORD({_name}, _default)',
            'i': 'SVE_INT({_name}, _default)',
            'd': 'SVE_DOUBLE({_name}, _default)',
            'iro': 'SVE_INT_READONLY({_name}, _default)',
            'cr': 'SVE_CHARREF({_name}, _ref)',
            'br': 'SVE_BYTEREF({_name}, _ref)',
            'sr': 'SVE_SHORTREF({_name}, _ref)',
            'ur': 'SVE_USHORTREF({_name}, _ref)',
            'ir': 'SVE_INTREF({_name}, _ref)',
            'fr': 'SVE_FLOATREF({_name}, _ref)',
            'br': 'SVE_BOOLREF({_name}, _ref)',
            'dwr': 'SVE_DWORDREF({_name}, _ref)',
            'dr': 'SVE_DOUBLEREF({_name}, _ref)',
            'drb': 'SVE_DWORDREF_BIT({_name}, _ref, _bit)',
            'drbr': 'SVE_DWORDREF_BIT_REVERSE({_name}, _ref, _bit)',
            'brb': 'SVE_BYTEREF_BIT({_name}, _ref, _bit)',
            'urb': 'SVE_USHORTREF_BIT({_name}, _ref, _bit)',
            'cv': 'SVE_CHAR_VALID_CHECK({_name}, _default)',
            'bv': 'SVE_BYTE_VALID_CHECK({_name}, _default)',
            'uv': 'SVE_USHORT_VALID_CHECK({_name}, _default)',
            'iv': 'SVE_INT_VALID_CHECK({_name}, _default)',
            'dv': 'SVE_DOUBLE_VALID_CHECK({_name}, _default)',
            'byv': 'SVE_BYTEREF_VALID_CHECK({_name}, _ref)',
            'urv': 'SVE_USHORTREF_VALID_CHECK({_name}, _ref)',
            'irv': 'SVE_INTREF_VALID_CHECK({_name}, _ref)',
        }

okSysValues = os.path.join(os.environ['Develop'], r'Source\vc32\okern96\okSysValues.cpp')
def sys_value_format(name, codestype): return ('\t\t' + codes[codetype] + ',').format(_name=name)
table_sign = 'static SYSVALUE l_values[] ='

while True:
    try:
        user = input('''-------------------Code Type:-------------------
{}
System Variable Name & Code type: '''.format('\n'.join(['{}\t{}'.format(k, v) for k, v in codes.items()])))
        if len(user) == 0:
            break
        name, codetype = user.split(' ')
        name = name.upper()

        with open(okSysValues) as fr:
            data = fr.read()

        table_begin = data.find(table_sign)
        table_begin += len(table_sign)
        table_end = data.find('\t};', table_begin)
        table = data[table_begin:table_end]

        sys_values = list(table.split('\n'))
        for i,line in enumerate(sys_values):
            m = re.search(r'SVE_[^(]*\(([0-9A-Z]+),', line)
            if m and name < m.group(1):
                sys_values.insert(i, sys_value_format(name, codetype))
                break
        else:
            sys_values.insert(len(sys_values)-1, sys_value_format(name, codetype))

        data = data[:table_begin] + '\n'.join(sys_values) + data[table_end:]

        with open(okSysValues, 'w') as fw:
            fw.write(data)
    except Exception as e:
        print(repr(e))
