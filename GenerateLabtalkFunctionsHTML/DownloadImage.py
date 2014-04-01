import sys
import os
import re
import subprocess
from urllib.request import urlretrieve
import urllib.error
from shutil import rmtree
from time import sleep

import inspect
currentpath = os.path.dirname(inspect.getfile(inspect.currentframe()))


def download_images(lang):
    htmlfile = os.path.join(currentpath, 'Default%s.html' % lang)

    if not os.path.isfile(htmlfile):
        return (False, "%s is needed to download images" % htmlfile)

    imagefolder = os.path.join(currentpath, 'images')
    try:
        rmtree(imagefolder)
    except FileNotFoundError:
        pass

    sleep(1)

    os.mkdir(imagefolder)

    def download(images, imagesfail):
        for image in images:
            image = image.replace('<img src="./images/', 'http://wikis/images/ltwiki/math/')
            slash = image.rfind('/')
            imagename = image[slash+1:]

            try:
                urlretrieve(image, os.path.join(imagefolder, imagename))
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                imagesfail.append(image)
            except Exception as e:
                return (False, "Failed to download %s : %s" % (imagename, e))

        return (True, "All images downloaded")

    with open(htmlfile, encoding='utf-8-sig') as fr:
        s = fr.read()
        images = re.findall('<img src="[^"]+', s)

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
