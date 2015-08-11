import os
import re
from datetime import datetime


okSysValues = os.path.join(os.environ['Develop'],
                           r'Source\vc32\okern96\okSysValues.cpp')

p_SVE = re.compile(r'^\s+SVE_[^(]+\((\w+)')
p_comment = re.compile(r'//.*?(\d+)[-/](\d+)[-/](\d+).*$')
p_comment_one_line = re.compile(r'^\s+//.*?(\d+)[-/](\d+)[-/](\d+).*$')

with open(okSysValues) as f:
    data = f.readlines()
    sysvars = []
    for i, line in enumerate(data):
        m = p_SVE.search(line)
        if m:
            comment = p_comment.search(line)
            if not comment:
                for j in range(10):
                    pre_line = data[i-j-1]
                    comment = p_comment_one_line.search(pre_line)
                    if comment or pre_line.find('//') >= 0:
                        break
            if comment:
                sysvars.append((m.group(1), comment))

date_formats = (
        '%m-%d-%Y',
        '%m-%d-%y',
        '%Y-%m-%d',
        )
date_cmp = datetime(2015, 1, 1)
p_comment_detail = re.compile(r'^//\W*(\w+).*?((QA|ORG|org)[-_]\d+)')
with open('new_sys_vars.txt', 'w') as fw:
    for sysvar in sysvars:
        var, comment = sysvar
        for fmt in date_formats:
            try:
                date = datetime.strptime('{}-{}-{}'.format(comment.group(1),
                                                           comment.group(2),
                                                           comment.group(3)),
                                         fmt)
                break
            except Exception:
                pass
        if date >= date_cmp:
            comment_detail = p_comment_detail.search(comment.group(0).lstrip())
            print('{}\t{}\t{}'.format(var, comment_detail.group(1), comment_detail.group(2)), file=fw)
