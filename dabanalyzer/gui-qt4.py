# -*- coding: utf-8 -*-
import os,sys
import imghdr
from time import sleep, ctime, time
from PyQt4 import QtCore, QtGui

class GUIQt(QtGui.QMainWindow):

  def __init__(self,*args):
    QtGui.QMainWindow.__init__(self,*args)
    self.setWindowTitle("DAB Analyzer")
    self.resize(800,600)
    self.time = time()
    self.dir_name = None
    self.last_path = ''
    self.status_bar = QtGui.QStatusBar(self)
    self.setStatusBar(self.status_bar)

    root = QtGui.QWidget()
    grid_lay = QtGui.QGridLayout(root)
    self.setCentralWidget(root)
    self.error_window = QtGui.QErrorMessage(root)

    self.box0 = QtGui.QGroupBox("", root)
    self.box0.setToolTip("Global threshold for DAB-positive area, from 0 to 100.\nOptimal values are usually located from 35 to 55.\nDefault 40.")
    self.box0.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
    lay0 = QtGui.QHBoxLayout(self.box0)
    self.check_thr = QtGui.QCheckBox("Thresh", self.box0)
    self.check_thr.setMinimumHeight(30)
    self.spin_thr = QtGui.QSpinBox()
    self.spin_thr.setFixedWidth(60)
    self.spin_thr.setRange(1, 100)
    self.slider_thr = QtGui.QSlider(QtCore.Qt.Horizontal, self.box0)
    self.slider_thr.setRange(1, 100)
    self.check_thr.stateChanged.connect(self.thresh_proc)
    self.thresh_proc(QtCore.Qt.Unchecked)
    self.connect(self.spin_thr, QtCore.SIGNAL("valueChanged(int)"), self.slider_thr, QtCore.SLOT("setValue(int)"))
    self.connect(self.slider_thr, QtCore.SIGNAL("valueChanged(int)"), self.spin_thr, QtCore.SLOT("setValue(int)"))
    self.spin_thr.setValue(40)
    lay0.addWidget(self.check_thr)
    lay0.addWidget(self.spin_thr)
    lay0.addWidget(self.slider_thr)
    grid_lay.addWidget(self.box0,0,0,1,8)

    self.box1 = QtGui.QGroupBox("", root)
    self.box1.setToolTip("Global threshold for EMPTY area, from 0 to 100.\nDefault disabled.")
    self.box1.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
    lay1 = QtGui.QHBoxLayout(self.box1)
    self.check_emp = QtGui.QCheckBox("EMPTY", self.box1)
    self.check_emp.setMinimumHeight(30)
    self.slider_emp = QtGui.QSlider(QtCore.Qt.Horizontal, self.box1)
    self.slider_emp.setRange(1, 100)
    self.spin_emp = QtGui.QSpinBox(self.box1)
    self.spin_emp.setFixedWidth(60)
    self.spin_emp.setRange(1, 100)
    self.check_emp.stateChanged.connect(self.empty_proc)
    self.empty_proc(QtCore.Qt.Unchecked)
    self.connect(self.spin_emp, QtCore.SIGNAL("valueChanged(int)"), self.slider_emp, QtCore.SLOT("setValue(int)"))
    self.connect(self.slider_emp, QtCore.SIGNAL("valueChanged(int)"), self.spin_emp, QtCore.SLOT("setValue(int)"))
    lay1.addWidget(self.check_emp)
    lay1.addWidget(self.spin_emp)
    lay1.addWidget(self.slider_emp)
    grid_lay.addWidget(self.box1,1,0,2,8)

    self.check_an = QtGui.QCheckBox("Analyze", root)
    self.check_an.setToolTip("Add group analysis after the indvidual image processing.\nThe groups are created using the filename.\nEverything before '_' symbol will be recognized as a group name.\nExample: sample01_10.jpg, sample01_11.jpg will be counted as a single group 'sample01'.\nDefault disabled.")
    grid_lay.addWidget(self.check_an,3,0)

    self.check_sil = QtGui.QCheckBox("Silent", root)
    self.check_sil.setToolTip("Supress figure rendering during the analysis,\nonly final results will be saved.\nDefault disabled.")
    grid_lay.addWidget(self.check_sil,4,0)

    self.box2 = QtGui.QGroupBox("", root)
    self.box2.setToolTip("Your matrix in a JSON formatted file.\nExperimental option.\nDefault use built-in.")
    lay2 = QtGui.QVBoxLayout(self.box2)
    self.check_mat = QtGui.QCheckBox("Matrix", self.box2)
    self.label_json = QtGui.QLabel("", self.box2)
    self.check_mat.stateChanged.connect(self.loadJSON)
    lay2.addWidget(self.check_mat)
    lay2.addWidget(self.label_json)
    grid_lay.addWidget(self.box2,3,1,2,7)

    self.user_frame = QtGui.QFrame(root)
    lay5 = QtGui.QVBoxLayout(self.user_frame)

    self.user_frame.setFrameShape(QtGui.QFrame.NoFrame)
    self.box3 = QtGui.QGroupBox("", self.user_frame)
    self.box3.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
    lay3 = QtGui.QVBoxLayout(self.box3)
    self.open_dir = QtGui.QPushButton('Open directory', self.box3)
    self.connect(self.open_dir, QtCore.SIGNAL('clicked()'), self.showDir)
    self.open_dir.setToolTip("Select directory with images for analyzing.")
    self.list_dir = QtGui.QListWidget(self.box3)
    self.list_dir.setToolTip("Names of images in current directory.\nSelect any for preview.\nRepeat click on current for deleting preview")
    self.list_dir.currentRowChanged.connect(self.showImage)
    self.list_dir.itemClicked.connect(self.showImage)
    self.label_dir = QtGui.QLineEdit("",self.box3)
    self.label_dir.setToolTip("Name of current directory.")
    self.label_dir.setReadOnly(True)
    lay3.addWidget(self.open_dir)
    lay3.addWidget(self.label_dir)
    lay3.addWidget(self.list_dir)

    box4 = QtGui.QGroupBox("", self.user_frame)
    lay4 = QtGui.QVBoxLayout(box4)
    self.run_button = QtGui.QPushButton('Run test', box4)
    self.run_button.clicked.connect(self.stub)
    self.image_field = QtGui.QLabel(box4)
    self.image_view = QtGui.QPixmap()
    self.image_field.setPixmap(self.image_view)
    self.log_output_field = QtGui.QTextEdit()
    self.log_output_field.setReadOnly(True)
    lay4.addWidget(self.run_button)
    lay4.addWidget(self.image_field)
    self.image_field.setVisible(False)
    lay4.addWidget(self.log_output_field)

    split = QtGui.QSplitter(1)
    split.addWidget(self.box3)
    split.addWidget(box4)
    lay5.addWidget(split)
    grid_lay.addWidget(self.user_frame,5,0,6,8)

    grid_lay.setRowStretch(5,1)
    grid_lay.setColumnStretch(3,2)
    grid_lay.setColumnStretch(4,3)
    grid_lay.setColumnStretch(5,2)
    self.stub_flag = False

  def stub(self):
    if self.stub_flag == True:
      self.stub_flag = False
    else:
      self.stub_flag = True
    self.freeze(self.stub_flag)

  def freeze(self, state):
    for i in [self.box0, self.box1, self.box2, self.box3, self.check_an, self.check_sil]:
      i.setDisabled(state)

  def showImage(self):
    if time() - self.time < 0.3:
      return
    number = self.list_dir.currentRow()
    name = self.list_dir.item(number).text()
    if self.status_bar.currentMessage().startswith(name):
      self.status_bar.showMessage("")
      self.image_field.setVisible(False)
      self.log_output_field.setVisible(True)
    else:
      if self.log_output_field.isVisible():
        self.log_output_field.setVisible(False)
        self.image_field.setVisible(True)
      full_name = os.path.join(self.dir_name, name)
      stat = os.stat(full_name)
      size = self.greek(stat.st_size)
      create_time = ctime(stat.st_mtime)
      self.status_bar.showMessage(name + ", " + size + ", " + create_time)
      self.image_view.load(full_name)
      rect = QtCore.QSize(self.image_field.width(),self.image_field.height())
      self.image_view = self.image_view.scaled(rect, 1)
      self.image_field.setPixmap(self.image_view)
      self.time = time()

  def greek(self, size):
    """Return a string representing the greek/metric suffix of a size"""
    _abbrevs = [(1<<50, 'PB'),(1<<40, 'TB'),(1<<30, 'GB'),(1<<20, 'MB'),(1<<10, 'kB'),(1, 'B')]
    for factor, suffix in _abbrevs:
      if size > factor:
        break
    return str(round(size/factor,2)) + suffix

  def thresh_proc(self, event):
    if event == QtCore.Qt.Unchecked:
      self.spin_thr.setVisible(False)
      self.slider_thr.setVisible(False)
    else:
      self.spin_thr.setVisible(True)
      self.slider_thr.setVisible(True)

  def empty_proc(self, event):
    if event == QtCore.Qt.Unchecked:
      self.spin_emp.setVisible(False)
      self.slider_emp.setVisible(False)
    else:
      self.spin_emp.setVisible(True)
      self.slider_emp.setVisible(True)

  def loadJSON(self, event):
    if event == QtCore.Qt.Unchecked:
      self.label_json.setText("")
      return
    self.json = QtGui.QFileDialog.getOpenFileNameAndFilter(self, 'Open file', self.last_path, 'JSON files (*.json)', 'JSON files (*.json)')[0]
    if self.json:
      self.last_path = os.path.dirname(self.json)
      self.label_json.setText("Selected: %s" %self.json)
    else:
      self.check_mat.setCheckState(QtCore.Qt.Unchecked)

  def showDir(self, dir_name = None):
    if not dir_name:
      dir_name = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory', self.last_path)
    if dir_name:
      files = [name for name in os.listdir(dir_name) if
              os.path.isfile(os.path.join(dir_name,name)) if
              imghdr.what(os.path.join(dir_name, name))]
      if len(files) == 0:
        self.error_window.showMessage("You need select directory with image(s)")
      else:
        self.last_path = self.dir_name = dir_name
        self.label_dir.setText(self.dir_name)
        self.list_dir.clear()
        self.list_dir.addItems(sorted(files))

  def showLog(self, log):
    if not self.log_output_field.isVisible():
      self.image_field.setVisible(False)
      self.log_output_field.setVisible(True)
    self.log_output_field.setText(log)
    self.status_bar.showMessage("")

  def getPath(self):
    if not self.dir_name:
      return None
    else:
      return self.dir_name

  def setPath(self, path):
    self.last_path = self.dir_name = path
    self.showDir(path)

  def getThresh(self):
    if self.check_thr.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return slider_thr.value()

  def setThresh(self, thr):
    self.check_thr.setCheckState(QtCore.Qt.Checked)
    self.spin_thr.setValue(thr)

  def getEmpty(self):
    if self.check_emp.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return slider_emp.value()

  def setEmpty(self, emp):
    self.check_emp.setCheckState(QtCore.Qt.Checked)
    self.spin_emp.setValue(thr)

  def getAnalyze(self):
    if self.check_an.checkState() == QtCore.Qt.Unchecked:
      return False
    else:
      return True

  def setAnalyze(self):
    self.check_an.setCheckState(QtCore.Qt.Checked)

  def getSilent(self):
    if self.check_sil.checkState() == QtCore.Qt.Unchecked:
      return False
    else:
      return True

  def setSilent(self):
    self.check_sil.setCheckState(QtCore.Qt.Checked)

  def getMatrix(self):
    if self.check_mat.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return self.json

  def setMatrix(self, json):
    self.check_mat.setCheckState(QtCore.Qt.Checked)
    self.last_path = os.path.dirname(json)
    self.json = json
    self.label_json.setText("Selected: %s" %self.json)

  def setAll(self, args):
    if args.json:
      self.setMatrix(args.json)
    if args.path:
      self.setPath(args.path)
    if args.thresh:
      self.setThresh(args.thresh)
    if args.empty:
      self.setEmpty(args.empty)
    if args.analyze:
      self.setAnalyze()
    if args.silent:
      self.setSilent()

  def getAll(self, args):
    args.path = self.getPath()
    args.thresh = self.getThresh()
    args.empty = self.getEmpty()
    args.analyze = self.getAnalyze()
    args.silent = self.getSilent()
    args.json = self.getMatrix()
    return args

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    aw = GUIQt()
    aw.show()
    sys.exit(app.exec_())
