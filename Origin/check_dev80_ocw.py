import os


with open(os.path.join(os.environ['Develop'], 'Origin', 'dev80.ocw')) as f:
    data1 = f.read().lower()
with open(os.path.join(os.environ['Develop'], 'Origin', 'dev80op.ocw')) as f:
    data2 = f.read().lower()
with open('res.txt', 'w') as fw:
    for root, firs, files in os.walk(os.path.join(os.environ['Develop'], 'Origin', 'OriginC')):
        for f in files:
            if f.lower().endswith('c') or f.lower().endswith('cpp'):
                if data1.find(f.lower()) < 0 and data2.find(f.lower()) < 0:
                    print(f, file=fw)
