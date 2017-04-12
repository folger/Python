import os
import sys
import traceback
import json
import queue
import threading
import tkinter as tk
from tkinter import messagebox as MB
from tkinter import filedialog as FD

from folstools.myutils import notepad_messagebox
from BatchBuildUtils import origin_version, copy_dlls


class Dlg(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        root.title('Copy Dlls')
        root.resizable(False, False)
        self.pack()
        self.initUI()

    def initUI(self):
        l1 = tk.Label(self, text='Develop Path')
        self.path = tk.StringVar()
        path = tk.Entry(self, width=40, textvariable=self.path)
        browse = tk.Button(self, text=' ... ',
                           command=self.browse_folder)
        self.win32 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Win32', variable=self.win32)
        self.x64 = tk.IntVar()
        c2 = tk.Checkbutton(self, text='x64', variable=self.x64)
        self.copy = tk.Button(self, text=' Copy ', command=self.do_copy)
        self.text = tk.Text(self, width=40, height=15)
        self.text['state'] = 'disabled'

        self.columnconfigure(3, pad=7)
        self.rowconfigure(0, pad=7)
        self.rowconfigure(5, weight=1)

        l1.grid(padx=5)
        path.grid(row=0, column=1, columnspan=2)
        browse.grid(row=0, column=3, padx=5, sticky=tk.W + tk.E)
        c1.grid(row=1, column=3, sticky=tk.W)
        c2.grid(row=2, column=3, sticky=tk.W)
        self.copy.grid(row=3, column=3, padx=5, sticky=tk.W + tk.E)
        self.text.grid(row=1, rowspan=5, columnspan=3,
                       padx=5, pady=5,
                       sticky=tk.W + tk.E + tk.N + tk.S)

    def do_copy(self):
        if not os.path.isdir(self.path.get()):
            self.showError('Invalid Develop Path')
            return
        platforms = []
        if self.win32.get():
            platforms.append(True)
        if self.x64.get():
            platforms.append(False)
        if not platforms:
            self.showError('Please check Win32/x64')
            return
        self.queue = queue.Queue()
        self.queue.put(platforms)
        self.queue.put(self)
        CopyTask(self.queue).start()

    def browse_folder(self):
        path = FD.askdirectory()
        if path:
            self.path.set(path)

    def showError(self, s):
        MB.showinfo('Error', s)


class CopyTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        try:
            platforms = self.queue.get(0)
            dlg = self.queue.get(0)
            path = dlg.path.get()
            copy = dlg.copy
            self.text = dlg.text
            with open('settings.json') as f:
                settings = json.load(f)
            self.version = origin_version(path, settings['MasterVersion'])

            copy['state'] = 'disabled'
            for p in platforms:
                copy_dlls(os.path.join(path, 'Origin'), p,
                          self.version, self.updated)
            copy['state'] = 'normal'
            self.output('Done ~~~')
        except:
            notepad_messagebox(traceback.format_exc())

    def updated(self, i, s):
        if i < 0:
            self.output(s)
        else:
            self.output('[{}] ({}) {}'.format(self.version, i + 1, s))

    def output(self, s):
        self.text['state'] = 'normal'
        self.text.insert(tk.END, s + '\n')
        self.text.see(tk.END)
        self.text['state'] = 'disabled'


root = tk.Tk()
app = Dlg(root)
app.mainloop()
