# -*- coding: utf-8 -*-
import os, sys
if sys.version_info.major == 3:
  import tkinter as tk
  import tkinter.filedialog as dialog
  from PIL import Image, ImageTk
else:
  import Image, ImageTk
  import tkFileDialog as dialog
  import Tkinter as tk
from time import sleep
import imghdr
import argparse
import subprocess as sp

class got:
  '''Prepare values for work in independent mode'''
  #__module__ = os.path.splitext(os.path.basename(__file__))[0]
  '''This string for right work of pickle'''

  def __init__(self):
    self.path = None
    self.thresh = 40
    self.matrix = None
    self.empty = 101
    self.silent = False
    self.analyze = False
    self.gui = 0

  def __repr__(self):
    return ' '.join("%s=%s" %(a, b) for a, b in self.__dict__.items())

class GUI:
  '''This class draw GUI window and set variables for manage calculates'''

  def parse(self, args):
    '''Parse arguments, copied from main cycle.'''
    if type(args) is not list:
      return args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False)
    parser.add_argument("-t", "--thresh", required=False, type=int, default=40)
    parser.add_argument("-e", "--empty", required=False, type=int, default=101)
    parser.add_argument("-s", "--silent", required=False, action="store_true")
    parser.add_argument("-a", "--analyze", required=False, action="store_true")
    parser.add_argument("-m", "--matrix", required=False)
    parser.add_argument("-g", "--gui", required=False, type=int, default = 0)
    arguments = parser.parse_args(args)
    return arguments

  def getPath(self, path = None):
    '''Get full path on target directory and show list images in this directory'''
    if self.flag:
      return
    if not path:
      path = self.init_path.show()
    if path:
      self.path = path
      self.butDir.config( text = "Opened:\n%s" %path)
    else:
      return
    file_len = 0
    self.files = [name for name in sorted(os.listdir(self.path))
            if not os.path.isdir(os.path.join(self.path, name))
            if imghdr.what(os.path.join(self.path, name))]
    self.dir_list.delete(0, 'end')
    if not self.files:
      self.dir_list.insert('end', "This directory not  have an images. Try select other.")
      self.path = None
      return
    for i in self.files:
      self.dir_list.insert('end', i)

  def setParam(self):
    '''Initial set inside variables, getted from main cycle; changed values in GUI window'''
    if self.args.path:
      self.init_path.options['initialdir'] = self.args.path
      self.init_json.options['initialdir'] = self.args.path
    if self.args.thresh != 40:
      self.thr_s.config(state = 'normal')
      self.thr_s.set(self.args.thresh)
      self.thr_v.set(True)
      self.thr_c.select()
    if self.args.empty != 101:
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
    '''Show preview image in selected directory. This function is not required, only for convenience' sake'''
    x = y = 1
    size = 400, 300
    self.preview.delete('1.0', 'end')
    i = self.dir_list.nearest(event.y)
    im = Image.open(os.path.join(self.path, self.files[i]))
    im.thumbnail(size, Image.ANTIALIAS)
    imag = ImageTk.PhotoImage(im)
    self.preview.image_create(1.0 ,image = imag)
    self.preview.image = imag

  def thr_f(self):
    '''Processing "Threshold" checkbutton event'''
    i = self.thr_v.get()
    if i == True:
      self.thr_s.config(state = 'normal')
    else:
      self.thr_s.config(state = 'disabled')

  def emp_f(self):
    '''Processing "EMPTY" checkbutton event'''
    i = self.emp_v.get()
    if i == True:
      self.emp_s.config(state = 'normal')
    else:
      self.emp_s.config(state = 'disabled')

  def mat_f(self):
    '''Processing "Matrix" checkbutton event'''
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

  def prepare(self):
    '''Getting all parameters, check flag for main cycle, freeze all controls'''
    ret = ''
    if self.path:
      self.args.path = self.path
      ret += '+-p+"%s"' %self.path
    else:
      self.dir_list.delete(0, 'end')
      self.dir_list.insert(0, 'You need select non-empty directory')
      return
    if self.thr_v.get():
      self.args.thresh = self.thr_s.get()
      ret += '+-t+'+ str(self.args.thresh)
    else:
      self.args.thresh = 40
    if self.emp_v.get():
      self.args.empty = self.emp_s.get()
      ret += '+-e+'+ str(self.args.empty)
    else:
      self.args.empty = 101
    if self.sil_v.get():
      self.args.silent = True
      ret += '+-s'
    else:
      self.args.silent = False
    if self.ana_v.get():
      self.args.analyze = True
      ret += '+-a'
    else:
      self.args.analyze = False
    if self.mat_v.get():
      self.args.matrix = self.json
      ret += '+-m+"%s"' %self.json
    else:
      self.args.matrix = None
    if __name__ == '__main__':
      if self.args.__class__.__name__ is 'got' or self.args.gui == 7:
        proc = sp.Popen([sys.executable + ' -u ' + os.path.abspath(os.path.dirname(__file__)) + "/dab_deconv_area.py " + ret.replace("+", " ")], shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        self.preview.delete(1.0, 'end')
        self.runBack()
        while True:
          self.loop(False)
          i = proc.stdout.readline()
          if not i or proc.poll() is not None:
            break
          self.preview.insert('end', i)
          if self.cancel:
            proc.terminate()
        self.final(False)
      else:
        print(ret.replace('"', ''))
        self.root.quit()
    else:
      self.runBack()

  def runBack(self):
    self.runBut.config(text = "Cancel", command = self.yesCancel)
    for i in [self.thr_c, self.thr_s, self.emp_c, self.emp_s, self.ana_c, self.sil_c, self.mat_c]:
      i.config(state = 'disabled')
    self.flag = True

  def yesCancel(self):
    '''Check flag for cancelling calculates'''
    self.cancel = True
    raise KeyboardInterrupt  # for mode 3 out from loop
    self.final()

  def final(self, renew = True):
    '''Out after calculates, unfreeze controls, print result log'''
    self.cancel = False
    self.flag = False
    for i in [self.thr_c, self.emp_c, self.ana_c, self.sil_c, self.mat_c]:
      i.config(state = 'normal')
    self.emp_f()
    self.thr_f()
    self.runBut.config( text="Run test", command=self.prepare)
    if renew:
      with open(os.path.join(self.path, "result", "log.txt")) as log:
        self.preview.delete(1.0, 'end')
        i = log.readline()
        while i:
          self.preview.insert('end', i)
          i = log.readline()

  def main(self):
    '''Prepare main GUI window.
    Variables name structure: xxx_y:
    xxx - first chars from parameter (DAB, EMPTY, silent, analyze, matrix),
    y: "v" -- BooleanVar, "s" -- scale, "c" -- checkbutton'''
    self.root = tk.Tk()
    self.root.minsize("800", "600")
    optframe = tk.Frame(self.root)
    optframe.pack(side = 'top')
    fileframe = tk.Frame(self.root)
    fileframe.pack(side = 'left')
    imgframe = tk.Frame(self.root)
    imgframe.pack()

    self.runBut = tk.Button(imgframe, text="Run test", command=self.prepare)
    self.runBut.pack(anchor = 'n')
    tk.Frame(imgframe, height=2, bd=1, relief='sunken').pack(side = 'top', fill='x')

    self.preview = tk.Text(imgframe, height=22, width = 65)
    scroll0=tk.Scrollbar(imgframe, borderwidth = 1, width = 8, bg = "grey")
    scroll0['command']=self.preview.yview
    self.preview['yscrollcommand']=scroll0.set
    scroll0.pack(side='right', fill ="y")
    self.preview.pack()
    self.butDir = tk.Button(fileframe, text = 'Select source directory', command = self.getPath)
    self.butDir.pack(side = 'top')
    self.init_path = dialog.Directory(fileframe, initialdir = None, mustexist = True, title = 'Select source directory')

    self.dir_list = tk.Listbox(fileframe, height=20, width = 65)
    scroll1=tk.Scrollbar(fileframe, borderwidth = 1, width = 8, bg = "grey")
    scroll1['command']=self.dir_list.yview
    self.dir_list['yscrollcommand']=scroll1.set
    scroll1.pack(side='right', fill ="y")
    self.dir_list.pack(side='bottom', fill='x')
    self.dir_list.bind('<Button-1>', self.click)

    self.thr_v = tk.BooleanVar()
    self.thr_c = tk.Checkbutton(optframe, indicatoron = 1, variable = self.thr_v, onvalue = True, offvalue = False, text = "Global threshold for DAB-positive area, from 0 to 100. Optimal values are usually located from 35 to 55.\n Default 40", command = self.thr_f)
    self.thr_c.pack(anchor = 'w')
    self.thr_s = tk.Scale(optframe, to = 100, length = 700,  orient = 'horizontal')
    self.thr_s['from'] = 1
    self.thr_s.set(40)
    self.thr_s.pack(anchor = 'e')
    self.thr_s['state'] = 'disabled'
    tk.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.emp_v = tk.BooleanVar()
    self.emp_c = tk.Checkbutton(optframe, indicatoron = 2, variable = self.emp_v, onvalue = True, offvalue = False, text = "Global threshold for EMPTY area, from 0 to 100.\n Default disabled", command = self.emp_f)
    self.emp_c.pack(anchor = 'w')
    self.emp_s = tk.Scale(optframe, to = 100, length = 700,  orient = 'horizontal', state = 'disabled')
    self.emp_s['from'] = 1
    self.emp_s.pack(anchor = 'e')
    tk.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.sil_v = tk.BooleanVar()
    self.sil_c = tk.Checkbutton(optframe, indicatoron = 1, variable = self.sil_v, onvalue = True, offvalue = False, text = "Supress figure rendering during the analysis, only final results will be saved")
    self.sil_c.pack(anchor = 'w')
    tk.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.ana_v = tk.BooleanVar()
    self.ana_c = tk.Checkbutton(optframe, indicatoron = 1, variable = self.ana_v, onvalue = True, offvalue = False, text = "Add group analysis after the indvidual image processing.\nThe groups are created using the filename.\nEverything before '_' symbol will be recognized as a group name.\nExample: sample01_10.jpg, sample01_11.jpg will be counted as a single group 'sample01'")
    self.ana_c.pack(anchor = 'w')
    tk.Frame(optframe, height=2, bd=1, relief='sunken').pack(fill='x')

    self.mat_v = tk.BooleanVar()
    self.mat_c = tk.Checkbutton(optframe, indicatoron = 1, variable = self.mat_v, onvalue = True, offvalue = False, text = "Your matrix in a JSON formatted file. Experimental option\n", command = self.mat_f)
    self.mat_c.pack(anchor = 'w')

    myfiletypes = [('JSON files', '.json'), ('All files', '*')]
    self.init_json = dialog.Open(optframe, initialdir = None, title = 'Select matrix file', filetypes = myfiletypes, defaultextension = '.json')
    tk.Frame(optframe, height = 2, width = 800, bd = 3, relief = 'solid').pack(fill='x')

  def loop(self, cycle):
    '''Substitution `root.mainloop()` for running as module'''
    while cycle:
      self.root.update()
      self.root.update_idletasks()
      sleep(0.2)
    else:
      self.root.update()
      self.root.update_idletasks()
      #sleep(.01)

  def __init__(self, args = None):
    '''Initialization inside variables, call prepares'''
    self.path = self.json = ''
    self.flag = self.cancel = False
    self.main()
    if args:
      self.args = self.parse(args)
      self.setParam()
      if self.args.path:
        self.getPath(self.args.path)
    else:
      self.args = got()

if __name__ == '__main__':
  '''Load parameters from main file across pickled container'''
  gui = GUI(sys.argv[1:])
  gui.root.mainloop()
