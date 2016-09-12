# -*- coding: utf-8 -*-
import os,sys
import imghdr
from time import sleep, ctime, time
from PyQt4 import QtCore, QtGui

class GUIQt(QtGui.QWidget):

  def __init__(self,*args):
    QtGui.QWidget.__init__(self,*args)
    self.setWindowTitle("DAB Analyzer")
    self.resize(800,600)
    box_lay = QtGui.QVBoxLayout(self)
    self.time = time()
    self.dir_name = None
    self.last_path = ''
    self.error_window = QtGui.QErrorMessage(self)

    self.frame = QtGui.QFrame(self)
    self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
    self.frame.setFrameShadow(QtGui.QFrame.Raised)
    grid_lay = QtGui.QGridLayout(self.frame)

    box0 = QtGui.QGroupBox("", self.frame)
    box0.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
    lay0 = QtGui.QHBoxLayout(box0)
    self.check_thr = QtGui.QCheckBox("Thresh", box0)
    self.check_thr.setMinimumHeight(30)
    self.spin_thr = QtGui.QSpinBox()
    self.spin_thr.setFixedWidth(60)
    self.spin_thr.setRange(1, 100)
    self.slider_thr = QtGui.QSlider(QtCore.Qt.Horizontal, box0)
    self.slider_thr.setRange(1, 100)
    self.check_thr.stateChanged.connect(self.thresh_proc)
    self.thresh_proc(QtCore.Qt.Unchecked)
    self.connect(self.spin_thr, QtCore.SIGNAL("valueChanged(int)"), self.slider_thr, QtCore.SLOT("setValue(int)"))
    self.connect(self.slider_thr, QtCore.SIGNAL("valueChanged(int)"), self.spin_thr, QtCore.SLOT("setValue(int)"))
    self.spin_thr.setValue(40)
    lay0.addWidget(self.check_thr)
    lay0.addWidget(self.slider_thr)
    lay0.addWidget(self.spin_thr)
    grid_lay.addWidget(box0,0,0,1,8)

    box1 = QtGui.QGroupBox("", self.frame)
    box1.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
    lay1 = QtGui.QHBoxLayout(box1)
    self.check_emp = QtGui.QCheckBox("EMPTY", box1)
    self.check_emp.setMinimumHeight(30)
    self.slider_emp = QtGui.QSlider(QtCore.Qt.Horizontal, box1)
    self.slider_emp.setRange(1, 100)
    self.spin_emp = QtGui.QSpinBox(box1)
    self.spin_emp.setFixedWidth(60)
    self.spin_emp.setRange(1, 100)
    self.check_emp.stateChanged.connect(self.empty_proc)
    self.empty_proc(QtCore.Qt.Unchecked)
    self.connect(self.spin_emp, QtCore.SIGNAL("valueChanged(int)"), self.slider_emp, QtCore.SLOT("setValue(int)"))
    self.connect(self.slider_emp, QtCore.SIGNAL("valueChanged(int)"), self.spin_emp, QtCore.SLOT("setValue(int)"))
    lay1.addWidget(self.check_emp)
    lay1.addWidget(self.slider_emp)
    lay1.addWidget(self.spin_emp)
    grid_lay.addWidget(box1,1,0,2,8)

    self.check_an = QtGui.QCheckBox("Analyze", self.frame)
    grid_lay.addWidget(self.check_an,3,0)

    self.check_sil = QtGui.QCheckBox("Silent", self.frame)
    grid_lay.addWidget(self.check_sil,4,0)

    box2 = QtGui.QGroupBox("", self.frame)
    lay2 = QtGui.QVBoxLayout(box2)
    self.check_mat = QtGui.QCheckBox("Matrix", box2)
    self.label_json = QtGui.QLabel("", box2)
    lay2.addWidget(self.check_mat)
    lay2.addWidget(self.label_json)
    grid_lay.addWidget(box2,3,1,2,7)
    self.check_mat.stateChanged.connect(self.loadJSON)

    box3 = QtGui.QGroupBox("", self.frame)
    box3.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
    lay3 = QtGui.QVBoxLayout(box3)
    self.open_dir = QtGui.QPushButton('Open directory', box3)
    self.connect(self.open_dir, QtCore.SIGNAL('clicked()'), self.showDir)
    self.open_dir.setToolTip("Open your mind")
    self.list_dir = QtGui.QListWidget(box3)
    self.list_dir.currentRowChanged.connect(self.showImage)
    self.list_dir.itemClicked.connect(self.showImage)
    self.label_dir = QtGui.QLineEdit("",box3)
    self.label_dir.setReadOnly(True)
    lay3.addWidget(self.open_dir)
    lay3.addWidget(self.label_dir)
    lay3.addWidget(self.list_dir)
    grid_lay.addWidget(box3,5,0,6,4)

    box4 = QtGui.QGroupBox("", self.frame)
    lay4 = QtGui.QVBoxLayout(box4)
    self.run_button = QtGui.QPushButton('Run test', box4)
    self.run_button.clicked.connect(self.getPath)
    self.image_box = QtGui.QGroupBox("", box4)
    image_lay = QtGui.QVBoxLayout(self.image_box)
    self.image_stats = QtGui.QLabel(self.image_box)
    self.image_view = QtGui.QPixmap()
    self.image_stats.setPixmap(self.image_view)
    self.log_output_field = QtGui.QTextEdit(self.image_box)
    self.log_output_field.setReadOnly(True)
    self.log_output_field.setText('fgn\nb')
    image_lay.addWidget(self.image_stats)
    self.image_stats.setVisible(False)
    image_lay.addWidget(self.log_output_field)
    lay4.addWidget(self.run_button)
    lay4.addWidget(self.image_box)
    grid_lay.addWidget(box4,5,4,6,5)

    grid_lay.setRowStretch(5,1)
    grid_lay.setColumnStretch(3,2)
    grid_lay.setColumnStretch(4,3)
    grid_lay.setColumnStretch(5,2)
    box_lay.addWidget(self.frame)

  def showImage(self):
    if time() - self.time < 0.3:
      return
    number = self.list_dir.currentRow()
    name = self.list_dir.item(number).text()
    if self.image_box.title().startswith(name):
      self.image_box.setTitle("")
      self.image_stats.setVisible(False)
      self.log_output_field.setVisible(True)
    else:
      if self.log_output_field.isVisible():
        self.log_output_field.setVisible(False)
        self.image_stats.setVisible(True)
      full_name = os.path.join(self.dir_name, name)
      stat = os.stat(full_name)
      size = self.greek(stat.st_size)
      create_time = ctime(stat.st_mtime)
      self.image_box.setTitle(name + ", " + size + ", " + create_time)
      self.image_box.update()
      self.image_view.load(full_name)
      rect = QtCore.QSize(self.image_stats.width(),self.image_stats.height())
      self.image_view = self.image_view.scaled(rect, 1)
      self.image_stats.setPixmap(self.image_view)
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

  def showDir(self):
    dir_name = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', self.last_path)
    if dir_name:
      files = [name for name in os.listdir(dir_name) if
              os.path.isfile(os.path.join(dir_name,name)) if
              imghdr.what(os.path.join(dir_name, name))]
      if len(files) == 0:
        self.error_window.showMessage("You need select directory with images")
      else:
        self.last_path = self.dir_name = dir_name
        self.label_dir.setText(self.dir_name)
        self.list_dir.clear()
        self.list_dir.addItems(sorted(files))

  def showLog(self, log):
    if not self.log_output_field.isVisible():
      self.image_stats.setVisible(False)
      self.log_output_field.setVisible(True)
    self.log_output_field.setText(log)
    self.image_box.setTitle("")

  def getPath(self):
    if not self.dir_name:
      return None
    else:
      return self.dir_name

  def getThresh(self):
    if self.check_thr.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return slider_thr.value()

  def getEmpty(self):
    if self.check_emp.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return slider_emp.value()

  def getAnalyze(self):
    if self.check_an.checkState() == QtCore.Qt.Unchecked:
      return False
    else:
      return True

  def getSilent(self):
    if self.check_sil.checkState() == QtCore.Qt.Unchecked:
      return False
    else:
      return True

  def getMatrix(self):
    if self.check_mat.checkState() == QtCore.Qt.Unchecked:
      return None
    else:
      return self.json


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    aw = GUIQt()
    aw.show()
    sys.exit(app.exec_())
