import sys
import os
import json
import traceback
from xml.etree import ElementTree as ET

from folstools.orglab import googledoc

try:
    with open('LocalXml.json', encoding='utf-8') as f:
        settings = json.load(f)

    langs, trans = googledoc.generate_localization_strings(settings['Doc'],
                                                           settings['Sheet'],
                                                           settings['Languages'],
                                                           settings['Category'])

    print('Generating XML ...')
    def get_tran(s, l):
        s = s.strip().replace('\r', '')
        try:
            return trans[s][l]
        except:
            print('{}: {}'.format(l, s))
            return s

    def write_xml(tree, path):
        fname = os.path.join(path, 'Localization.xml')
        print(fname)
        with open(fname, 'w', encoding='utf-8') as f:
            tree.write(f, encoding='unicode')

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
            write_xml(tree, os.path.join(GRAPHING, f))

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

    write_xml(tree, ANALYSIS)
except Exception:
    traceback.print_exc()
finally:
    os.system('pause')
