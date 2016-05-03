#!/usr/bin/python3

from tkinter import *

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image

from kuntze.oneBadge import oneBadge

__author__ = 'Mathias Kuntze'


def createBadges(imagePath, title, txtPath, saveName, root, textbox, progress):

    fontName = 'agency-fb'

    image = Image.open(imagePath)
    image_width, image_height = image.size

    badge_width = 9*cm

    badge_height = 6*cm

    c = canvas.Canvas(saveName, pagesize=[badge_width, badge_height])

    txtObj = open(txtPath)
    num = 0
    for line in txtObj:
        num += 1

    step = 100.0/num

    i = 0
    error_num = 0
    txtObj = open(txtPath)
    for line in txtObj:
        i += 1
        fontSize = 50
        person = line.rstrip()
        person_array = person.split(';')
        if len(person_array) != 3:
            print('error line ' + str(i))
            error_num += 1
            continue
        name = person_array[0].strip()
        nickname = person_array[1].strip()
        grade = person_array[2].strip()
        if not name:
            print('error line ' + str(i))
            error_num += 1
            continue

        oneBadge(c, imagePath, name, title, grade, badge_width=badge_width, badge_height=badge_height, font_name=fontName)
        oneBadge(c, imagePath, nickname, title, grade, badge_width=badge_width, badge_height=badge_height, font_name=fontName)

        progress.step(step)
        root.after(200, textbox.insert(END, 'generated '+str(i) + ' / ' + name + '; ' + nickname + '; ' + grade + '\n'))
        root.update()
        textbox.see(END)


    c.save()

    root.after(200, textbox.insert(END, '\n\n\nprocess is finished! ' + str(error_num) + ' errors'))
    root.update()
    textbox.see(END)
