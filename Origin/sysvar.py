import os
import re


codes = {
        'v': 'FUNC_SYS_VALUE_VAR_DEF({_name}, TYPE, _defaultVal)',
        'vr': 'FUNC_SYS_VALUE_VAR_DEF_READONLY({_name}, TYPE, _defaultVal)',
        'vv': 'static bool FUNC_VALID_CHECK({_name})(double& value)\n{{\n\treturn true;\n}}\nFUNC_SYS_VALUE_VAR_DEF_VALID_CHECK({_name}, TYPE, _defaultVal)',
        'gb': 'FUNC_SYS_VALUE_GSTATE_BIT({_name}, _field, _bit)',
        'gbr': 'FUNC_SYS_VALUE_GSTATE_BIT_REVERSE({_name}, _field, _bit)',
        'gv': 'FUNC_SYS_VALUE_GSTATE_VAR({_name}, _field)',
        'gvv': 'static bool FUNC_VALID_CHECK({_name})(double& value)\n{{\n\treturn true;\n}}\nFUNC_SYS_VALUE_GSTATE_VAR_VALID_CHECK({_name}, _field)',
        'f': 'FUNC_SYS_VALUE_FUNC_DEF({_name}, _func)',
        'fr': 'FUNC_SYS_VALUE_READONLY({_name}, [](){{return;}})',
        'fg': 'FUNC_SYS_VALUE_GENERAL({_name}, [](){{return;}}, [](double val){{;}})',
        'vc': 'static double FUNC_GET_CONVERT({_name})(int value)\n{{\n\treturn 0;\n}}\nstatic int FUNC_SET_CONVERT({_name})(double value)\n{{\n\treturn 0;\n}}\nFUNC_SYS_VALUE_VAR_DEF_CONVERT({_name}, TYPE, _defaultVal)',
        'cb': 'FUNC_SYS_VALUE_COMMON_DWORD_BIT({_name}, _bit, _bReverseBVal)',
        'z':'FUNC_SYS_VALUE_DEF({_name})\n{{\n\treturn 1;\n}}',
        }

okSysValues = os.path.join(os.environ['Develop'], r'Source\vc32\okern96\okSysValues.cpp')
def sys_value_format(name): return '\t\t_SVE({}),'.format(name)
table_sign = 'static SYSVALUE l_values[] = {'

while True:
    try:
        user = input('''Code Type:
v     FUNC_SYS_VALUE_VAR_DEF(_name, TYPE, _defaultVal)
vr    FUNC_SYS_VALUE_VAR_DEF_READONLY(_name, TYPE, _defaultVal)
vv    FUNC_SYS_VALUE_VAR_DEF_VALID_CHECK(_name, TYPE, _defaultVal)
gb    FUNC_SYS_VALUE_GSTATE_BIT(_name, _field, _bit)
gbr   FUNC_SYS_VALUE_GSTATE_BIT_REVERSE(_name, _field, _bit)
gv    FUNC_SYS_VALUE_GSTATE_VAR(_name, _field)
gvv   FUNC_SYS_VALUE_GSTATE_VAR_VALID_CHECK(_name, _field)
f     FUNC_SYS_VALUE_FUNC_DEF(_name, _func)
fr    FUNC_SYS_VALUE_READONLY(_name, _func)
fg    FUNC_SYS_VALUE_GENERAL(_name, _funcGet, _funcSet)
vc    FUNC_SYS_VALUE_VAR_DEF_CONVERT(_name, TYPE, _defaultVal)
cb    FUNC_SYS_VALUE_COMMON_DWORD_BIT(_name, _bit, _bReverseBVal)
z     FUNC_SYS_VALUE_DEF(_name)
System Variable Name & Code type: ''')
        if len(user) == 0:
            break
        name, codetype = user.split(' ')
        name = name.upper()

        with open(okSysValues) as fr:
            data = fr.read()

        func_pos = data.find('template <class T, int N>')
        data = data[:func_pos] + codes[codetype].format(_name=name) + '\n' + data[func_pos:]

        table_begin = data.find(table_sign)
        table_begin += len(table_sign)
        table_end = data.find('}', table_begin)
        table = data[table_begin:table_end]

        sys_values = list(table.split('\n'))
        for i,line in enumerate(sys_values):
            m = re.search(r'_SVE\(([0-9A-Z]+)\)', line)
            if m and name < m.group(1):
                sys_values.insert(i, sys_value_format(name))
                break
        else:
                sys_values.insert(len(sys_values)-1, sys_value_format(name))

        data = data[:table_begin] + '\n'.join(sys_values) + data[table_end:]

        with open(okSysValues, 'w') as fw:
            fw.write(data)
    except Exception as e:
        print(repr(e))
