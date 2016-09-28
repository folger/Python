import traceback
import GeneratePolishedHTML
import DownloadImage
from GenerateLTFuncHTML import HTMLType


print("""What do you want ?

1. Generate HTML
2. Download Images
""")

while True:
    try:
        choice = int(input("Choose one operation, or press any other to quit : ").strip())
        try:
            if 1 == choice:
                valid_langs = ['E', 'J', 'G', 'All']
                language = input('Languages({}) ? '.format(', '.join(valid_langs)))
                if language not in valid_langs:
                    print('Invalid language !!!!!')
                    continue
                languages = ('E', 'G', 'J') if language == "All" else (language,)
                for language in languages:
                    for htmlType in (HTMLType.SCV, HTMLType.FO, HTMLType.NLFIT):
                        GeneratePolishedHTML.generate_HTML(language, htmlType)
                print('Done !!!!!')
            elif 2 == choice:
                print(DownloadImage.download_images('E')[1])
        except:
            print(traceback.format_exc())
    except:
        break
