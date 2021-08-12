import GeneratePolishedHTML
import DownloadImage
from GenerateLTFuncHTML import GenerateXML

while 1:
    jobs = input('''What to do ? (Can be combined)
E: English HTML files
J: Japanese HTML files
C: Chinese HTML files
X: Functions XML file
I: Image files
(EJCXI): ''')
    if not jobs:
        break
    for job in jobs:
        if job in 'EJG':
            print(f'Generating {job} html files ... ', end='', flush=True)
            GeneratePolishedHTML.generate_HTML(job)
            print('Done')
        elif job == 'X':
            print(f'Generating Functions.xml ... ', end='', flush=True)
            generate = GenerateXML()
            generate.Exec()
            print('Done')
        elif job == 'I':
            print('Downloading images ... ')
            result = DownloadImage.download_images()
            print(result[1])
