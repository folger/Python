import os
import re

okSysValues = os.path.join(os.environ['Develop'], r'Source\vc32\okern96\okSysValues.cpp')

with open(okSysValues) as fr:
    data = fr.read()

gstates = []
for line in data.split('\n'):
    m = re.match(r'FUNC_SYS_VALUE_GSTATE_BIT_REVERSE\((\w+),\s(\w+),\s([^,]+)\).*', line)
    if m:
        gstates.append(m)

for gstate in gstates:
    data = data.replace(gstate.group(0) + '\n', '')
    data = data.replace('_SVE({})'.format(gstate.group(1)), '_SVE_DWORDPTR_BIT_REVERSE({}, &g_lpCentralStatus->{}, {})'.format(gstate.group(1), gstate.group(2), gstate.group(3)))

with open(okSysValues, 'w') as fw:
    fw.write(data)
