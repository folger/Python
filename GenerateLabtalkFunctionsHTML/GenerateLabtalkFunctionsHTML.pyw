import sys
import threading
import tkinter as tk
from tkinter import messagebox as MB

import GeneratePolishedHTML
import DownloadImage
from GenerateLTFuncHTML import GenerateXML


class GenerateHTMLDlg(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        root.title('Generate Labtalk Functions HTML')
        root.resizable(False, False)
        self.pack()
        self.initUI()

    def initUI(self):
        lang_group = tk.LabelFrame(self, text=' Language ', padx=5, pady=5)
        self._langs = []
        lang = tk.IntVar()
        self._langs.append((lang, tk.Checkbutton(lang_group, text='E',
                                                 variable=lang)))
        lang = tk.IntVar()
        self._langs.append((lang, tk.Checkbutton(lang_group, text='G',
                                                 variable=lang)))
        lang = tk.IntVar()
        self._langs.append((lang, tk.Checkbutton(lang_group, text='J',
                                                 variable=lang)))
        self.generate_html = tk.Button(lang_group, text=' Generate HTML ',
                                       command=self.generateHTML)
        for lang in self._langs:
            lang[1].pack(side=tk.LEFT)
        self.generate_html.pack(side=tk.LEFT, padx=5)

        self.generate_xml = tk.Button(self, text='     Generate XML    ',
                                      command=self.generateXML)
        self.download_images = tk.Button(self, text=' Download Images ',
                                         command=self.downloadImages)

        lang_group.grid(rowspan=2, padx=5, pady=5)
        self.generate_xml.grid(row=0, column=1, padx=5, pady=5)
        self.download_images.grid(row=1, column=1, padx=5, pady=(0, 5))

    def generateHTML(self):
        languages = []
        for lang in self._langs:
            if lang[0].get():
                languages.append(lang[1]['text'])
        for language in languages:
            GeneratePolishedHTML.generate_HTML(language)
        self.reportResult((True, 'Done'))

    def generateXML(self):
        generate = GenerateXML()
        generate.Exec()
        self.reportResult((True, 'Done'))

    def downloadImages(self):
        result = DownloadImage.download_images()
        self.reportResult(result)

    def reportResult(self, result):
        if result[0]:
            MB.showinfo('Attention', result[1])
        else:
            MB.showerror('Error', result[1])

root = tk.Tk()
app = GenerateHTMLDlg(root)
app.mainloop()
