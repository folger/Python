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
    def __init__(self, master):
        super().__init__(master)
        master.title('Copy Dlls')
        master.resizable(False, False)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.win32 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Win32', variable=self.win32)
        self.x64 = tk.IntVar()
        c2 = tk.Checkbutton(self, text='x64', variable=self.x64)

        browse = tk.Button(self, text='Develop Path',
                           command=self.ask_directory)
        self.path = tk.StringVar()
        path = tk.Entry(self, width=50, textvariable=self.path)
        self.copy = tk.Button(self, text='Copy', command=self.do_copy)
        self.text = tk.Text(self, width=50, height=20)

        browse.grid(row=0, column=0, sticky=tk.W + tk.E)
        path.grid(row=0, column=1, columnspan=2)
        c1.grid(row=1, column=0, sticky=tk.W)
        c2.grid(row=1, column=1, sticky=tk.W)
        self.copy.grid(row=1, column=2, sticky=tk.W + tk.E)
        self.text.grid(row=2, columnspan=3)

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

    def ask_directory(self):
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
        except:
            notepad_messagebox(traceback.format_exc())

    def updated(self, i, s):
        if i < 0:
            self.output(s)
        else:
            self.output('[{}] ({}) {}'.format(self.version, i + 1, s))

    def output(self, s):
        self.text.insert(tk.END, s + '\n')
        self.text.see(tk.END)


root = tk.Tk()
app = Dlg(root)
app.mainloop()
