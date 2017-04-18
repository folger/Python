import sys
import os
import re
import subprocess
from urllib.request import urlretrieve
import urllib.error
from shutil import rmtree
from time import sleep
from xml.etree import ElementTree as ET

import bs4
import LTFuncsHTMLParser

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))
if not currentpath:
    currentpath = os.getcwd()


def download_images():
    xmlfile = os.path.join(currentpath, 'Functions.xml')

    if not os.path.isfile(xmlfile):
        return (False, "%s is needed to download images" % xmlfile)

    imagelang = 'images'
    imagefolder = os.path.join(currentpath, imagelang)
    try:
        rmtree(imagefolder)
    except FileNotFoundError:
        pass

    sleep(1)

    os.mkdir(imagefolder)

    def download(images, imagesfail):
        httpprefix = LTFuncsHTMLParser.get_http_prefix('E')
        for image in images:
            image = httpprefix + image
            slash = image.rfind('/')
            imagename = image[slash + 1:]

            try:
                urlretrieve(image, os.path.join(imagefolder, imagename))
            except Exception as e:
                imagesfail.append(image)

        return (True, "All images downloaded")

    images = []
    tree = ET.parse(xmlfile)
    for elem in tree.iter():
        imgs = elem.get('images')
        if imgs:
            images += imgs.split('|')

    subprocess.Popen(r'explorer %s' % imagefolder)

    imagesfail = []
    while True:
        result = download(images, imagesfail)
        if not result[0] or len(imagesfail) == 0:
            return result

        images = imagesfail[:]
        imagesfail.clear()


if __name__ == "__main__":
    result = download_images(sys.argv[1])
    print(result[1])
