import os
import json
from xml.etree import ElementTree as ET

from folstools.orglab import googledoc

langs, trans = googledoc.generate_localization_strings('LocalizeLog_94', 'Additional File', 'OriginCentral')


def get_tran(s, l):
    s = s.strip().replace('\r', '')
    try:
        return trans[s][l]
    except:
        print('{}: {}'.format(l, s))
        return s


GRAPHING = './Graphing'
for f in os.listdir(GRAPHING):
    if os.path.isdir(os.path.join(GRAPHING, f)):
        root = ET.Element('Root')
        tree = ET.ElementTree(root)
        for l in langs:
            lang = ET.Element(l)
            root.append(lang)
            project = ET.Element('Project')
            lang.append(project)
            name = ET.Element('Name')
            name.text = get_tran(f, l)
            project.append(name)
        with open(os.path.join(GRAPHING, f, 'Localization.xml'), 'w', encoding='utf-8') as f:
            tree.write(f, encoding='unicode')

ANALYSIS = './Analysis'
with open(os.path.join(ANALYSIS, 'Analysis_E.json')) as f:
    js = json.load(f)

root = ET.Element('Root')
tree = ET.ElementTree(root)
for l in langs:
    lang = ET.Element(l)
    root.append(lang)
    for proj in js['Projects']:
        project = ET.Element('Project')
        lang.append(project)
        name = ET.Element('Name')
        name.text = get_tran(proj['ProjectName'], l)
        project.append(name)
        folders = ET.Element('Folders')
        project.append(folders)
        for fold in proj['Folders']:
            folder = ET.Element('Folder')
            folders.append(folder)
            name = ET.Element('Name')
            name.text = get_tran(fold['FolderName'], l)
            folder.append(name)
            hint = ET.Element('Hint')
            hint.text = get_tran(fold['Hint'], l)
            folder.append(hint)

with open(os.path.join(ANALYSIS, 'Localization.xml'), 'w', encoding='utf-8') as f:
    tree.write(f, encoding='unicode')
