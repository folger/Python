import os
import re
import json
import traceback


# {
# 	"modules": {
# 		"ok9": {
# 			"func1": "B8 04 00 00 00 C3"
# 		},
# 		"ok9_64": {
# 			"func2": "B8 04 00 00 00 C3"
# 		}
# 	}
# }
try:
    with open('settings.json') as f:
        settings = json.load(f)

    for module, funcs in settings['modules'].items():
        dllfile = module + '.dll'
        mapfile = module + '.map'
        try:
            for f in (dllfile, mapfile):
                if not os.path.isfile(f):
                    print(f + ' is missing')
                    raise ValueError
        except ValueError:
            continue

        with open(mapfile) as f:
            offsets = {}
            for line in f:
                line = line.strip()
                for funcname, _ in funcs.items():
                    m = re.search(r'\w{4}:(\w+)\s+\?' + funcname, line)
                    if m:
                        offsets[funcname] = int(m.group(1), 16) + 0x400
                if len(offsets) == len(funcs):
                    break
            for funcname, codes in funcs.items():
                offset = offsets.get(funcname)
                if not offset:
                    print('Fail to find offset for {}' + funcname)
                    continue
                with open(dllfile, 'rb') as f:
                    data = f.read()
                modified = bytes(bytearray.fromhex(codes))
                data = data[:offset] + modified + data[offset + len(modified):]
                with open(module + '_cracked.dll', 'wb') as f:
                    f.write(data)
        print('Successfully pack cracked dll for ' + module)
except Exception:
    traceback.print_exc()

os.system('pause')
