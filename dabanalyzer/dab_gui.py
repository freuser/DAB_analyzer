# -*- coding: utf-8 -*-
import Tkinter
import tkFileDialog
import os
import time
import argparse
import Image, ImageTk
#from PIL import Image, ImageTk

class GUI:

  def getPath(self, path = None):
      ext = ('.jpg', '.jpeg', '.gif', '.png')
      if not path:
        path = self.init_path.show()
      if path:
        self.path = path
      else:
        return
      file_len = 0
      self.files = [name for name in sorted(os.listdir(self.path))
              if not os.path.isdir(os.path.join(self.path, name))
              if name.endswith(ext)]
      self.dir_list.delete(0, 'end')
      for i in self.files:
        self.dir_list.insert('end', i)

  def parse(self, args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False)
    parser.add_argument("-t", "--thresh", required=False, type=int)
    parser.add_argument("-e", "--empty", required=False, type=int)
    parser.add_argument("-s", "--silent", required=False, action="store_true")
    parser.add_argument("-a", "--analyze", required=False, action="store_true")
    parser.add_argument("-m", "--matrix", required=False)
    arguments = parser.parse_args(args)
    return arguments

  def setParam(self):
    if self.args.path:
      self.initialdir = self.args.path
      self.init_path.options['initialdir'] = self.initialdir
      self.init_json.options['initialdir'] = self.initialdir
    if self.args.thresh:
      self.dab_s.config(state = 'normal')
      self.dab_s.set(self.args.thresh)
      self.dab_v.set(True)
      self.dab_c.select()
    if self.args.empty:
      self.emp_s.config(state = 'normal')
      self.emp_s.set(self.args.empty)
      self.emp_v.set(True)
      self.emp_c.select()
    if self.args.silent:
      self.sil_v.set(True)
      self.sil_c.select()
    if self.args.analyze:
      self.ana_v.set(True)
      self.ana_c.select()
    if self.args.matrix:
      self.mat_c.select()
      self.mat_v.set(True)
      self.json = self.args.matrix
      self.mat_c.config(text = 'Your matrix in a JSON formatted file. Experimental option.\nOpened file: %s' % self.json)

  def click(self, event):
    x = y = 1
    size = 300, 300
    self.img.delete('1.0', 'end')
    i = self.dir_list.nearest(event.y)
    im = Image.open(file = os.path.join(self.path, self.files[i]))
    im.thumbnail(size, Image.ANTIALIAS)
    imag = ImageTk.PhotoImage(im)
    self.img.image_create(1.0 ,image = imag)
    self.img.image = imag

  def dab_f(self):
    i = self.dab_v.get()
    if i == True:
      self.dab_s.config(state = 'normal')
    else:
      self.dab_s.config(state = 'disabled')

  def emp_f(self):
    i = self.emp_v.get()
    if i == True:
      self.emp_s.config(state = 'normal')
    else:
      self.emp_s.config(state = 'disabled')

  def mat_f(self):
    i = self.mat_v.get()
    if i == False:
      self.mat_c.deselect()
      self.mat_c.config(text = 'Your matrix in a JSON formatted file. Experimental option.\n')
    else:
      files = self.init_json.show()
      if files:
        self.mat_c.config(text = 'Your matrix in a JSON formatted file. Experimental option.\nOpened file: %s' %files)
        self.json = files
      else:
        self.mat_c.deselect()
        self.mat_c.config(text = 'Your matrix in a JSON formatted file. Experimental option.\n')

  def run(self):
    if self.path:
      self.args.path = self.path
    else:
      self.dir_list.delete(0, 'end')
      self.dir_list.insert(0, 'You need select directory')
      return
    if self.dab_v.get():
      self.args.thresh = self.dab_s.get()
    else:
      self.args.thresh = 40
    if self.emp_v.get():
      self.args.empty = self.emp_s.get()
    else:
      self.args.empty = 101
    if self.sil_v.get():
      self.args.silent = True
    else:
      self.args.silent = False
    if self.ana_v.get():
      self.args.analyze = True
    else:
      self.args.analyze = False
    if self.mat_v.get():
      self.args.matrix = self.json
    else:
      self.args.matrix = None
    self.flag = True
    time.sleep(3)
    self.runBut.config(text = "Cancel", command = self.yesCancel)

  def yesCancel(self):
    self.cancel = True

  def notCancel(self):
    self.runBut.config( text="Run test", command=self.run)
    with open(os.path.join(self.path, "result", "log.txt")) as log:
      self.img.delete(1.0, 'end')
      i = log.readline()
      while i:
        self.img.insert('end', i)
        i = log.readline()

  def main(self):
    self.root = Tkinter.Tk()
    self.root.minsize("800", "600")
    optframe = Tkinter.Frame(self.root)
    optframe.pack(side = 'top')
    fileframe = Tkinter.Frame(self.root)
    fileframe.pack(side = 'left')
    imgframe = Tkinter.Frame(self.root)
    imgframe.pack()

    self.img = Tkinter.Text(imgframe)
    scroll0=Tkinter.Scrollbar(imgframe, borderwidth = 1, width = 8, bg = "grey")
    scroll0['command']=self.img.yview
    self.img['yscrollcommand']=scroll0.set
    scroll0.pack(side='right', fill ="y")
    self.img.pack()
    Tkinter.Button(fileframe, text="Select source directory", command = self.getPath).pack(side = 'top')
    self.init_path = tkFileDialog.Directory(fileframe, initialdir = self.initialdir, mustexist = True, title = 'Select source directory')

    self.runBut = Tkinter.Button(imgframe, text="Run test", command=self.run)
    self.runBut.pack(anchor = 'n')
    Tkinter.Frame(imgframe, height=2, bd=1, relief='sunken').pack(side = 'top', fill='x')

    self.dir_list = Tkinter.Listbox(fileframe, height=20, width = 65)
    scroll1=Tkinter.Scrollbar(fileframe, borderwidth = 1, width = 8, bg = "grey")
    scroll1['command']=self.dir_list.yview
    self.dir_list['yscrollcommand']=scroll1.set
    scroll1.pack(side='right', fill ="y")
    self.dir_list.pack(side='bottom', fill='x')
    self.dir_list.bind('<Button-1>', self.click)

    self.dab_v = Tkinter.BooleanVar()
    self.dab_c = Tkinter.Checkbutton(optframe, indicatoron = 1, variable = self.dab_v, onvalue = True, offvalue = False, text = "Global threshold for DAB-positive area, from 0 to 100. Optimal values are usually located from 35 to 55.\n Default 40", command = self.dab_f)
    self.dab_c.pack(anchor = 'w')
    self.dab_s = Tkinter.Scale(optframe, to = 100, length = 700,  orient = 'horizontal')
    self.dab_s['from'] = 1
    self.dab_s.set(40)
    self.dab_s.pack(anchor = 'e')
    self.dab_s['state'] = 'disabled'
    Tkinter.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.emp_v = Tkinter.BooleanVar()
    self.emp_c = Tkinter.Checkbutton(optframe, indicatoron = 2, variable = self.emp_v, onvalue = True, offvalue = False, text = "Global threshold for EMPTY area, from 0 to 100.\n Default disabled", command = self.emp_f)
    self.emp_c.pack(anchor = 'w')
    self.emp_s = Tkinter.Scale(optframe, to = 100, length = 700,  orient = 'horizontal', state = 'disabled')
    self.emp_s['from'] = 1
    self.emp_s.pack(anchor = 'e')
    Tkinter.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.sil_v = Tkinter.BooleanVar()
    self.sil_c = Tkinter.Checkbutton(optframe, indicatoron = 1, variable = self.sil_v, onvalue = True, offvalue = False, text = "Supress figure rendering during the analysis, only final results will be saved")
    self.sil_c.pack(anchor = 'w')
    Tkinter.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.ana_v = Tkinter.BooleanVar()
    self.ana_c = Tkinter.Checkbutton(optframe, indicatoron = 1, variable = self.ana_v, onvalue = True, offvalue = False, text = "Add group analysis after the indvidual image processing.\nThe groups are created using the filename.\nEverything before '_' symbol will be recognized as a group name.\nExample: sample01_10.jpg, sample01_11.jpg will be counted as a single group 'sample01'")
    self.ana_c.pack(anchor = 'w')
    Tkinter.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.mat_v = Tkinter.BooleanVar()
    self.mat_c = Tkinter.Checkbutton(optframe, indicatoron = 1, variable = self.mat_v, onvalue = True, offvalue = False, text = "Your matrix in a JSON formatted file. Experimental option\n", command = self.mat_f)
    self.mat_c.pack(anchor = 'w')

    myfiletypes = [('JSON files', '.json'), ('All files', '*')]
    self.init_json = tkFileDialog.Open(optframe, initialdir = self.initialdir, title = 'Select matrix file', filetypes = myfiletypes, defaultextension = '.json')
    Tkinter.Frame(optframe, height = 2, width = 800, bd = 3, relief = 'solid').pack(fill='x')

  def loop(self):
    self.root.update()
    self.root.update_idletasks()

  def __init__(self, args):
    self.initialdir = '/home'
    self.path = self.json = ''
    self.flag = self.cancel = False
    self.main()
    if args:
      self.args = self.parse(args)
      self.setParam()
    self.getPath(self.initialdir)

if __name__ == '__main__':
  main()