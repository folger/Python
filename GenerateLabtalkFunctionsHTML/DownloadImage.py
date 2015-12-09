import sys
import os
import re
import subprocess
from urllib.request import urlretrieve
import urllib.error
from shutil import rmtree
from time import sleep
import LTFuncsHTMLParser

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))


def download_images(lang):
    htmlfile = os.path.join(currentpath, 'SCV_%s.html' % lang)

    if not os.path.isfile(htmlfile):
        return (False, "%s is needed to download images" % htmlfile)

    imagelang = 'images'
    imagefolder = os.path.join(currentpath, imagelang)
    try:
        rmtree(imagefolder)
    except FileNotFoundError:
        pass

    sleep(1)

    os.mkdir(imagefolder)

    def download(images, imagesfail):

        for image in images:
            image = image.replace('<img src="./{}/'.format(imagelang), LTFuncsHTMLParser.get_http_prefix(lang) + LTFuncsHTMLParser.get_image_path(lang))
            slash = image.rfind('/')
            imagename = image[slash+1:]

            try:
                urlretrieve(image, os.path.join(imagefolder, imagename))
            except Exception as e:
                imagesfail.append(image)

        return (True, "All images downloaded")

    with open(htmlfile, encoding='utf-8-sig') as fr:
        s = fr.read()
        images = list(set(re.findall('<img src="[^"]+', s)))

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
