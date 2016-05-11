# convert ui to py
# pyuic4 qtdesigner.ui -o qtdesigner.py
import sys

from PyQt4 import QtCore, QtGui, Qt
import os, subprocess

from gui import Ui_MainWindow
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image


from kuntze.oneBadge import oneBadge


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
__author__ = 'Mathias Kuntze'


class MyForm(QtGui.QMainWindow):
    backgroundFileTypes = dict(defaultextension='.jpg', filetypes=[('.jpg', '*.jpg')])
    textFileTypes = dict(defaultextension='.txt', filetypes=[('Text-Datei', '*.txt')])
    pdfFileTypes = dict(defaultextension='.pdf', filetypes=[('PDF', '*.pdf')])

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.backgroundPath = ""
        self.databasePath = ""
        self.outputPath = ""
        self.logoText = ""

        self.ui.button_next.clicked.connect(self.nextTab)
        self.ui.button_preview.clicked.connect(self.prevTab)
        self.ui.button_load_data.clicked.connect(self.loadDatabase)
        self.ui.button_start_generate.clicked.connect(self.generateBadges)
        self.ui.button_background.clicked.connect(self.loadBackground)
        self.ui.Tab.currentChanged.connect(self.tabHandler)

        self.ui.table_databases.setColumnCount(4)
        self.ui.table_databases.setRowCount(5)
        self.ui.table_databases.setHorizontalHeaderLabels(['Name', 'Spitzname', 'Studiengang', 'Jahr'])

    def nextTab(self):
        if self.ui.Tab.currentIndex() > 1:
            return

        self.ui.Tab.setCurrentIndex(self.ui.Tab.currentIndex()+1)

    def prevTab(self):
        if self.ui.Tab.currentIndex() < 1:
            return

        self.ui.Tab.setCurrentIndex(self.ui.Tab.currentIndex()-1)

    def loadDatabase(self):
        self.databasePath = QtGui.QFileDialog().getOpenFileName(caption = "Namen", filter="*.txt")
        if not self.databasePath:
            return

        self.ui.table_databases.clear()
        self.ui.table_databases.setColumnCount(4)
        self.ui.table_databases.setRowCount(0)
        self.ui.table_databases.setHorizontalHeaderLabels(['Name', 'Spitzname', 'Studiengang', 'Jahr'])
        reader = csv.reader(open(self.databasePath), delimiter=';')
        i = 0

        for row in reader:
            self.ui.table_databases.insertRow(i)
            self.ui.table_databases.setItem(i, 0, QtGui.QTableWidgetItem(row[0]))
            self.ui.table_databases.setItem(i, 1, QtGui.QTableWidgetItem(row[1]))
            self.ui.table_databases.setItem(i, 2, QtGui.QTableWidgetItem(row[2]))
            self.ui.table_databases.setItem(i, 3, QtGui.QTableWidgetItem(row[3]))
            i += 1

        self.ui.table_databases.resizeColumnsToContents()
        self.ui.table_databases.resizeRowsToContents()


    def loadBackground(self):
        self.backgroundPath = QtGui.QFileDialog().getOpenFileName(caption="Hintergrund", filter="*.jpg")
        pixmap = QtGui.QPixmap(self.backgroundPath)
        pixmap = pixmap.scaled(self.ui.label_bg_prev.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.label_bg_prev.setPixmap(pixmap)
        self.ui.label_bg_prev.show()
        self.ui.edit_path_bg.setText(self.backgroundPath)



    def generateBadges(self):

        progress_max = self.ui.table_databases.rowCount()
        self.ui.textarea_log.clear()

        fontName = 'agency-fb'
        fontPath = 'misc/fonts/'+fontName+'.ttf'
        pdfmetrics.registerFont(TTFont(fontName, fontPath))

        imagePath = self.backgroundPath
        self.logoText = self.ui.edit_title.text()

        if not imagePath:
            msg = QtGui.QMessageBox()
            msg.setText("Hintergrundbild muss angegeben werden!")
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setWindowTitle("Hintergrundbild fehlt")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            self.ui.Tab.setCurrentIndex(0)
            self.ui.button_preview.setDisabled(True)
            self.ui.button_next.setDisabled(False)
            return

        if not self.logoText:
            msg = QtGui.QMessageBox()
            msg.setText("Titel muss angegeben werden!")
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setWindowTitle("Titel fehlt")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            self.ui.Tab.setCurrentIndex(0)
            self.ui.button_preview.setDisabled(True)
            self.ui.button_next.setDisabled(False)
            return


        self.outputPath = QtGui.QFileDialog().getSaveFileName(caption = "Speicherort", filter="*.pdf")
        if not self.outputPath:
            return

        image = Image.open(imagePath)
        image_width, image_height = image.size

        badge_width = 9*cm
        badge_height = 6*cm

        c = canvas.Canvas(self.outputPath, pagesize=[badge_width, badge_height])

        title = self.ui.edit_title.text()
        if not title:
            title = 'Tutor'

        for i in range(1, progress_max+1):
            name = self.ui.table_databases.item(i-1,0)
            nick = self.ui.table_databases.item(i-1,1)
            sg = self.ui.table_databases.item(i-1,2)
            year = self.ui.table_databases.item(i-1,3)

            flag = []
            if name is None:
                flag.append("Name")
            if nick is None:
                flag.append("Spitzname")
            if sg is None:
                flag.append("Studiengang")
            if year is None:
                flag.append("Jahr")

            if len(flag) > 0:
                self.ui.textarea_log.append(str(i) + " Es fehlen Informationen: " + ', '.join(flag))
            else:
                a = sg.text() + "'" + year.text()
                oneBadge(c, imagePath, name.text(), title, a, badge_width=badge_width, badge_height=badge_height, font_name=fontName)
                oneBadge(c, imagePath, nick.text(), title, a, badge_width=badge_width, badge_height=badge_height, font_name=fontName)
                self.ui.textarea_log.append(str(i) + " Badge fuer " + name.text() + " wurde erzeugt.")

            percent = (100/progress_max)*i
            self.ui.progressbar.setValue(percent)
        self.ui.textarea_log.append("")
        self.ui.textarea_log.append("Alle Badges wurden erstellt und gespeichert (" + self.outputPath + ") !")
        c.save()

        if sys.platform == 'linux':
            subprocess.call(["xdg-open", self.outputPath])
        else:
            os.startfile(self.outputPath)

    def tabHandler(self, i):
        if i == 0:
            self.ui.button_preview.setDisabled(True)
            self.ui.button_next.setDisabled(False)
        if i == 2:
            self.ui.button_preview.setDisabled(False)
            self.ui.button_next.setDisabled(True)
        if i == 1:
            self.ui.button_preview.setDisabled(False)
            self.ui.button_next.setDisabled(False)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
