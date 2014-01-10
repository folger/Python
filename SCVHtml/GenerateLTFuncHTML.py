funcs_descriptions = {}
with open(r'C:\Dropbox\LTFuncs.txt', 'r') as f:
  for line in f:
    entries = line.split('\t'*10)
    funcs_descriptions[entries[0].split('(')[0].lower()] = (entries[0], entries[1] if len(entries) > 1 else "")

with open(r'C:\Dropbox\SCVFuncs.txt', 'r') as f:
  s = ''

  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue

    if line.endswith('$') or line.endswith(')'): # function
      try:
        funcs_description = funcs_descriptions[line.split('(')[0].lower()]
      except KeyError as e:
        pass
        # print("Missing function: %s" % line)
      s += '<tr><td><a href="/junk">%s</a></td><td>%s</td></tr>' % (funcs_description[0], funcs_description[1].strip())
    else: # category
      if len(s):
        s += '</table>'
      s += '<table><caption>%s</caption>' % line

  if len(s):
    s += '</table>'
  print(s)

