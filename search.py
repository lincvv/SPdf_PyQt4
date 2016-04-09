import os, subprocess
import sys

import re
from PyQt4 import QtGui
from PyQt4 import QtCore
# from PyQt4.examples.activeqt.webbrowser.ui_mainwindow import _translate

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class SearchFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        QtGui.QWidget.__init__(self, parent)
        color = QtGui.QColor(200, 200, 200)

        # self.widget = QtGui.QWidget(self)
        # self.widget.setStyleSheet("QWidget { background-color: %s }" % color.name())
        # self.widget.setGeometry(100, 50, 350, 300)

        self.setGeometry(250, 100, 350, 300)
        self.setStyleSheet("QWidget { background-color: %s }" % color.name())
        self.resize(850, 550)
        self.setWindowTitle('Spdf')
        # self.textEdit = QtGui.QTextEdit()
        # self.setCentralWidget(self.textEdit)
        pushButton = QtGui.QPushButton('Найти', self)
        pushButton.setGeometry(580, 460, 131, 31)
        color = QtGui.QColor(100, 255, 100)
        pushButton.setStyleSheet("QWidget { background-color: %s }" % color.name())
        pushButton.setObjectName(_fromUtf8("pushButton"))
        progressBar = QtGui.QProgressBar(self)
        progressBar.setGeometry(QtCore.QRect(40, 60, 751, 16))
        progressBar.setProperty("value", 0)
        progressBar.setObjectName(_fromUtf8("progressBar"))
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(300, 460, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        color = QtGui.QColor(255, 255, 250)
        self.lineEdit.setFont(font)
        self.lineEdit.setAutoFillBackground(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit.setStyleSheet("QWidget { background-color: %s }" % color.name())
        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(40, 80, 751, 361))
        self.textBrowser.setStyleSheet("QWidget { background-color: %s }" % color.name())
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textBrowser.setSizeIncrement(QtCore.QSize(2, 2))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.textBrowser.setFont(font)
        self.textBrowser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textBrowser.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setInputMethodHints(QtCore.Qt.ImhNone)
        self.textBrowser.setFrameShape(QtGui.QFrame.WinPanel)
        self.textBrowser.setTabChangesFocus(False)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lcdNumber = QtGui.QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(-60, 440, 221, 61))
        self.lcdNumber.setFrameShape(QtGui.QFrame.Box)
        self.lcdNumber.setFrameShadow(QtGui.QFrame.Sunken)
        self.lcdNumber.setLineWidth(0)
        self.lcdNumber.setMidLineWidth(0)
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))

        self.statusBar()
        self.setFocus()
        open = QtGui.QAction(QtGui.QIcon('open.gif'), 'Open', self)
        open.setShortcut('Ctrl+O')
        open.setStatusTip('Open new File')

        self.connect(open, QtCore.SIGNAL('triggered()'), self.showDialog)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(open)


        self.__MAX = 100

        self.text = self.lineEdit

        self.pic = self.textBrowser

        self.progress = progressBar

        self.set_val = 0
        self.lcd = self.lcdNumber


        self.connect(pushButton, QtCore.SIGNAL("clicked()"), lambda: self.search_file())
        self.connect(self.textBrowser, QtCore.SIGNAL("cursorPositionChanged()"), lambda: self.cursor())

# метод поиск файла с заданными буквами
    def search_file(self):
        text_find_count = []
        list_pdf = []
        pdf = self.text.text()
        self.pic.setText(" ")
        self.progress.reset()
        set_val = 0
        for i in os.listdir("."):
            list_pdf.extend(re.findall(r"[\w\-\.\s\(\)]+\.pdf|[\w\-\.\s]+\.PDF", i))
        if pdf:
            for i in list_pdf:
                name_file = i[:len(i) - 4]
                find_str = name_file.lower().find(str(pdf).lower())
                if find_str >= 0:
                    self.pic.append(i)
                    text_find_count.append(i)
                self.set_val += self.__MAX - (self.__MAX - len(text_find_count))
                self.progress.setValue(self.set_val)
                self.lcd.display(len(text_find_count))
                # print(len(text_find_count))
            self.progress.setValue(self.set_val + (self.__MAX - self.set_val))


        # map(lambda x: pic.append(x), text_find_suc)


    def cursor(self):
        if self.progress.value() == self.__MAX:
            browser_text = str(self.pic.toPlainText())
            pos = self.pic.textCursor()

            if pos.position() != 0:
                text_left = text_right = str()
                count_left = count_right = pos.position() - 1
                while(True):
                    if count_right != len(browser_text) and browser_text[count_right] != '\n':
                        text_right = text_right + browser_text[count_right]
                        count_right += 1
                    elif count_left != 0 and browser_text[count_left - 1] != '\n':
                        text_left = browser_text[count_left - 1] + text_left
                        count_left -= 1
                    else:
                        break
                pdf_open = text_left + text_right

                print(pdf_open)
                if sys.platform.startswith('darwin'):
                    subprocess.call(('open', pdf_open))
                elif os.name == 'nt':
                    os.startfile(pdf_open)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open',pdf_open))

        else:
            return 0

    def showDialog(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        # file = open(filename)
        # data = file.read()
        # self.textEdit.setText(data)
        try:
            os.chdir(filename)
        except OSError:
            return 0


app = QtGui.QApplication(sys.argv)
ui = SearchFile()
ui.show()
app.exec_()