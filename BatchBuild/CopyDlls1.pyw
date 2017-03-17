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
        path_group = tk.Frame(self)
        path_group.pack()
        l1 = tk.Label(path_group, text='Develop Path')
        l1.pack(side=tk.LEFT)
        self.path = tk.StringVar()
        path = tk.Entry(path_group, width=40, textvariable=self.path)
        path.pack(side=tk.LEFT)
        browse = tk.Button(path_group, text=' ... ',
                           command=self.browse_folder)
        browse.pack(side=tk.LEFT)

        self.win32 = tk.IntVar()
        c1 = tk.Checkbutton(path_group, text='Win32', variable=self.win32)
        c1.pack(side=tk.LEFT)
        self.x64 = tk.IntVar()
        c2 = tk.Checkbutton(path_group, text='x64', variable=self.x64)
        c2.pack(side=tk.LEFT)
        self.copy = tk.Button(path_group, text=' Copy ', command=self.do_copy)
        self.copy.pack(side=tk.LEFT)

        self.text = tk.Text(self, width=40, height=20)
        self.text['state'] = 'disabled'
        self.text.pack(fill=tk.BOTH)

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
