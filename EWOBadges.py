#!/usr/bin/env python3
# convert ui to py
# pyuic4 qtdesigner.ui -o qtdesigner.py
import csv
import os
import subprocess
import sys

from PyQt4 import QtCore, QtGui
from kuntze.oneBadge import oneBadge
from kuntze.resource import resource_path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from gui import Ui_MainWindow

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
    textFileTypes = dict(defaultextension='.txt', filetypes=[('Text-Datei', '*.txt'), ('CSV-Datei', '*.csv')])
    pdfFileTypes = dict(defaultextension='.pdf', filetypes=[('PDF', '*.pdf')])

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(_translate("MainWindow", "EWOBadges v1.2", None))

        self.backgroundPath = ""
        self.backgroundPath_2 = ""
        self.databasePath = ""
        self.outputPath = ""
        self.logoText = ""

        self.ui.button_next.clicked.connect(self.nextTab)
        self.ui.button_preview.clicked.connect(self.prevTab)
        self.ui.button_load_data.clicked.connect(self.loadDatabase)
        self.ui.button_start_generate.clicked.connect(self.generateBadges)
        self.ui.button_background.clicked.connect(self.loadBackground)
        self.ui.button_background_2.clicked.connect(self.loadBackground_2)
        self.ui.Tab.currentChanged.connect(self.tabHandler)

        self.ui.table_databases.setColumnCount(4)
        self.ui.table_databases.setRowCount(8)
        self.ui.table_databases.setHorizontalHeaderLabels(['Name', 'Spitzname', 'Studiengang', 'Jahr'])

    def nextTab(self):
        if self.ui.Tab.currentIndex() > 1:
            return

        self.ui.Tab.setCurrentIndex(self.ui.Tab.currentIndex() + 1)

    def prevTab(self):
        if self.ui.Tab.currentIndex() < 1:
            return

        self.ui.Tab.setCurrentIndex(self.ui.Tab.currentIndex() - 1)

    def loadDatabase(self):
        self.databasePath = QtGui.QFileDialog().getOpenFileName(caption="Namen", filter="CSV-Datei (*.txt *.csv)")
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

    # front page
    def loadBackground(self):
        self.backgroundPath = QtGui.QFileDialog().getOpenFileName(caption="Vorderseite", filter="*.jpg")
        pixmap = QtGui.QPixmap(self.backgroundPath)
        pixmap = pixmap.scaled(self.ui.label_bg_prev.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.label_bg_prev.setPixmap(pixmap)
        self.ui.label_bg_prev.show()
        self.ui.edit_path_bg.setText(self.backgroundPath)

    # back page
    def loadBackground_2(self):
        self.backgroundPath_2 = QtGui.QFileDialog().getOpenFileName(caption="Rückseite", filter="*.jpg")
        pixmap = QtGui.QPixmap(self.backgroundPath_2)
        pixmap = pixmap.scaled(self.ui.label_bg_prev_2.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.label_bg_prev_2.setPixmap(pixmap)
        self.ui.label_bg_prev_2.show()
        self.ui.edit_path_bg_2.setText(self.backgroundPath_2)

    def generateBadges(self):

        progress_max = self.ui.table_databases.rowCount()
        self.ui.textarea_log.clear()

        fontName = 'agency-fb'
        fontPath = resource_path('misc/fonts/' + fontName + '.ttf')
        pdfmetrics.registerFont(TTFont(fontName, fontPath))

        imagePath = self.backgroundPath
        imagePath_2 = self.backgroundPath_2
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

        if not imagePath_2:
            imagePath_2 = imagePath

        self.outputPath = QtGui.QFileDialog().getSaveFileName(caption="Speicherort", filter="*.pdf")
        if not self.outputPath:
            return

        badge_width = 9 * cm
        badge_height = 6 * cm

        c = canvas.Canvas(self.outputPath, pagesize=A4)  # pagesize=[2*badge_width, badge_height])

        title = self.ui.edit_title.text()
        if not title:
            title = 'Tutor'

        offset_bottom = 25
        offset_left = 40

        for i in range(1, progress_max + 1):
            name = self.ui.table_databases.item(i - 1, 0)
            nick = self.ui.table_databases.item(i - 1, 1)
            sg = self.ui.table_databases.item(i - 1, 2)
            year = self.ui.table_databases.item(i - 1, 3)

            rightText = list()

            if sg is not None:
                if sg.text() is not "":
                    rightText.append(sg.text())

            if year is not None:
                if year.text() is not "":
                    rightText.append(year.text())

            if name is not None:
                if name.text() is not "":
                    name = name.text()
                else:
                    name = ""
            else:
                name = ""

            if nick is not None:
                if nick.text() is not "":
                    nick = nick.text()
                else:
                    nick = ""
            else:
                nick = ""

            flag = []
            if name is "":
                flag.append("Name")
            if nick is "":
                flag.append("Spitzname")

            if len(flag) > 0:
                self.ui.textarea_log.append(str(i) + " Es fehlen Informationen: " + ', '.join(flag))

            if len(rightText) == 0:
                a = ""
            else:
                a = "'".join(rightText)

            oneBadge(c, imagePath, name, title, a, badge_width=badge_width, badge_height=badge_height,
                     font_name=fontName, offset=(offset_left, offset_bottom))
            oneBadge(c, imagePath_2, nick, '', a, badge_width=badge_width, badge_height=badge_height,
                     font_name=fontName, offset=(offset_left + badge_width, offset_bottom))

            if name is "" or name is None:
                self.ui.textarea_log.append(str(i) + " leerer Badge wurde erzeugt.")
            else:
                self.ui.textarea_log.append(str(i) + " Badge fuer " + name + " wurde erzeugt.")

            offset_bottom += badge_height + 25
            pagebreak = False
            if i % 4 == 0:
                offset_bottom = 25
                c.showPage()

            percent = (100 / progress_max) * i
            self.ui.progressbar.setValue(percent)
        self.ui.textarea_log.append("")
        self.ui.textarea_log.append("Alle Badges wurden erstellt und gespeichert (" + self.outputPath + ") !")

        c.setAuthor('StuRa TU Ilmenau')
        c.setTitle('Badges für die Erstiwoche TU Ilmenau')
        c.setCreator('EWOBadges.exe @Mathias Kuntze')
        c.setSubject('https://github.com/KuntzeM/EWOBadges')



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
