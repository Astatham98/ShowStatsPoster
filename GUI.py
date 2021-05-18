from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from stats import CreatePicture
import os
from colorpicker import ColorPicker
import shutil

#class Ui_MainWindow(object):
class UI_MainWindow(QMainWindow):
    def __init__(self):
        super(UI_MainWindow, self).__init__()
        self.currentShow = ""
        self.picked_color = (255, 255, 255)
        self.setupUi(self)
    
    def setupUi(self, MainWindow):        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(656, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.app = QApplication([])
        
        self.dialog = QFileDialog()
        
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(120, 700, 131, 41))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(lambda: self.save())
        
        self.newButton = QtWidgets.QPushButton(self.centralwidget)
        self.newButton.setGeometry(QtCore.QRect(410, 700, 131, 41))
        self.newButton.setObjectName("newButton")
        self.newButton.clicked.connect(lambda: self.resetScreen())
        
        self.title = QtWidgets.QTextBrowser(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(100, 10, 461, 61))
        self.title.setObjectName("title")
        
        self.seriesInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.seriesInput.setGeometry(QtCore.QRect(100, 110, 371, 31))
        self.seriesInput.setObjectName("seriesInput")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 90, 71, 16))
        self.label.setObjectName("label")
        
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(300, 200, 71, 16))
        self.errorLabel.setObjectName("error")
        self.errorLabel.setStyleSheet("color: red")
        
        
        self.colourInput = QtWidgets.QLabel(self.centralwidget)
        self.colourInput.setGeometry(QtCore.QRect(190, 160, 81, 51))
        self.colourInput.setObjectName("BlockColor")
        self.borderStylesheet()
  
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 140, 101, 16))
        self.label_2.setObjectName("label_2")
        
        self.seriesNameEnter = QtWidgets.QPushButton(self.centralwidget)
        self.seriesNameEnter.setGeometry(QtCore.QRect(480, 110, 81, 31))
        self.seriesNameEnter.setObjectName("seriesNameEnter")
        self.seriesNameEnter.clicked.connect(lambda: self.createImage())
        
        self.colourEnter = QtWidgets.QPushButton(self.centralwidget)
        self.colourEnter.setGeometry(QtCore.QRect(100, 160, 81, 51))
        self.colourEnter.setObjectName("colourEnter")
        self.colourEnter.clicked.connect(lambda: self.getColor())
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 656, 21))
        self.menubar.setObjectName("menubar")
        
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(120, 230, 400, 400)
        self.imgLabel.setObjectName('image')
        self.imgLabel.setText("")
        self.imgLabel.setScaledContents(True)
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionNew)
        
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.actionNew.triggered.connect(lambda: self.resetScreen())
        
        self.actionSave.triggered.connect(lambda: self.save())        


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Series rating generator."))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.newButton.setText(_translate("MainWindow", "New"))
        self.title.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt; font-weight:600;\">Series Rating Generator</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Series name"))
        self.errorLabel.setText(_translate("MainWindow", ""))
        self.seriesNameEnter.setText(_translate("MainWindow", "Enter"))
        self.colourEnter.setText(_translate("MainWindow", "Choose a color"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save image"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "New Image"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        
    def createImage(self):
        text = self.seriesInput.toPlainText()
        colour = '#%02x%02x%02x' % self.picked_color
        
        text = text.rstrip()
        text = text.lstrip()
        self.clearExceptions()
        
        if text != '':
            try:
                picture = CreatePicture(text, colour)
                picture.createImage()
                self.updatePhoto(text)
                self.currentShow = text
            except KeyError:
                self.updateErrorLabel('Enter a valid series (Movies dont work)')
        else:
            self.updateErrorLabel('Enter a valid series')
    
    def updateErrorLabel(self, text):
         self.errorLabel.setText(text)
         self.errorLabel.adjustSize()
         
    def updatePhoto(self, name):
        if self.currentShow != "":
            try:
                os.remove(self.currentShow + '.png')
            except FileNotFoundError:
                pass
        self.imgLabel.setPixmap(QtGui.QPixmap(name + '.png'))
            
    def resetScreen(self):
        self.imgLabel.setPixmap(QtGui.QPixmap(""))
        self.seriesInput.appendPlainText("")
        self.picked_color = (255, 255, 255)
        self.borderStylesheet()
        self.clearExceptions()
        
        try:
            os.remove(self.currentShow + '.png')
        except FileNotFoundError:
            pass
        
    def getColor(self):
        self.color_picker = ColorPicker()
        self.picked_color = self.color_picker.getColor()
        self.picked_color = tuple([int(x) for x in self.picked_color])
        self.borderStylesheet()
        
    def save(self):
        
        if self.currentShow != "":
            dir = self.chooseDir()
            show = self.currentShow + '.png'
            shutil.copy(show, dir)
            os.remove(show)
        else:
            self.updateErrorLabel('Please create a poster before saving')
    
    def chooseDir(self):
        self.dialog = QFileDialog()
        folder_path = self.dialog.getExistingDirectory(None, "Select Folder")
        return folder_path
    
    def closeEvent(self, event):
       if self.currentShow != "":
            try:
                os.remove(self.currentShow + '.png')
            except FileNotFoundError:
                pass
            
    def clearExceptions(self):
        self.errorLabel.setText("")
        
    def borderStylesheet(self):
        self.colourInput.setStyleSheet("""QWidget {{border: 1px solid black; border-radius: 2px; background-color: rgb{};}} """.format(self.picked_color))
           
    
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    MainWindow = UI_MainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
