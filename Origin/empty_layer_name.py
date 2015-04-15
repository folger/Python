import os
import re

path = 'H:/Dev/Origin/Localization/J'
pattern = re.compile(b'Pd\d' + 32 * b'\0')
count = 0
for f in os.listdir(path):
    if f.lower().endswith('.otp'):
        with open(os.path.join(path, f), 'rb') as fr:
            data = fr.read()
        al = pattern.findall(data)
        if len(al) > 0:
            with open(os.path.join(path, f), 'wb') as fw:
                print(f, len(al), sep=' ')
                count += 1
                fw.write(pattern.sub(b'Pd' + 33 * b'\0', data))
print(count)
