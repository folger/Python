import os
import re

path = 'H:/Dev/Origin'
pattern = re.compile(b'Pd\d' + 32 * b'\0')
count = 0
for f in os.listdir(path):
    if f.lower().endswith('.otp'):
        with open(os.path.join(path, f), 'rb') as fr:
            data = fr.read()
        data1 = pattern.sub(b'Pd' + 33 * b'\0', data)
        if data != data1:
            with open(os.path.join(path, f), 'wb') as fw:
                print(f)
                count += 1
                fw.write(data1)
print(count)
