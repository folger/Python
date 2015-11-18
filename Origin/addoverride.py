from collections import defaultdict


MAC_PATH = '/Users/gzmac/development'
WIN_PATH = 'H:'


lines = set()
with open('override.txt') as f:
    for line in f:
        if line.find('overrides a member function') > 0:
            lines.add(line.replace(MAC_PATH, WIN_PATH).rstrip())

warnings = defaultdict(set)
for line in lines:
    items = line.split(':')
    warnings[':'.join(items[0:2]).lower()].add(int(items[2])-1)

for k in sorted(warnings.keys()):
    with open(k) as f:
        lines = f.read().split('\n')
    for linenum in warnings[k]:
        line = lines[linenum]
        pos = line.find('{')
        if pos > 0:
            while True:
                if not line[pos-1].isspace():
                    break
                pos -= 1
        else:
            pos = line.find(';')
            if pos < 0:
                pos = len(line)
        lines[linenum] = line[:pos] + ' override' + line[pos:]
    with open(k, 'w') as f:
        f.write('\n'.join(lines))
