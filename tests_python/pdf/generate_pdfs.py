# -*- coding: utf-8 -*-
import os
import csv

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape, portrait

from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from mxdata import (where,
                    when,
                    program,
                    module,
                    volume,
                    director,
                    some_boss,
                    city,
                    diploma_info,
                    reg_number)


pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))


def build_diploma(person_data):
    diploma_fname = 'diplom%s.pdf' % person_data['diploma_id']
    path_to_diploma = os.path.join('diplomas', diploma_fname)

    doc = SimpleDocTemplate(
        path_to_diploma,
        pagesize=landscape(A4),
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER, fontname='Verdana'))

    story = []

    person = '<font size=8 name=Verdana>\
    %(family)s %(name)s %(patronymic)s</font>' % person_data
    story.append(Paragraph(person, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_where = '<font size=8 name=Verdana>\
    прошел(а) обучение в %(where)s\
    </font>' % where
    story.append(Paragraph(diploma_where, styles["Justify"]))

    diploma_when = '<font size=8 name=Verdana>\
    c «%(when_begin_day)s» %(when_begin_month)s %(when_begin_year)s \
    по «%(when_end_day)s» %(when_end_month)s %(when_end_year)s \
    </font>' % when
    story.append(Paragraph(diploma_when, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_program = '<font size=8 name=Verdana>%s</font>' % program
    story.append(Paragraph(diploma_program, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_module = '<font size=8 name=Verdana>%s</font>' % module
    story.append(Paragraph(diploma_module, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_volume = '<font size=8 name=Verdana>%s</font>' % volume
    story.append(Paragraph(diploma_volume, styles["Justify"]))
    story.append(Spacer(1, 8))
    story.append(Spacer(1, 8))

    diploma_director = '<font size=8 name=Verdana>%s</font>' % director
    story.append(Paragraph(diploma_director, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_some_boss = '<font size=8 name=Verdana>%s</font>' % some_boss
    story.append(Paragraph(diploma_some_boss, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_city = '<font size=8 name=Verdana>%s</font>' % city
    story.append(Paragraph(diploma_city, styles["Justify"]))
    story.append(Spacer(1, 8))

    diploma_diploma_info = '<font size=8 name=Verdana>%s</font>' % diploma_info
    story.append(Paragraph(diploma_diploma_info, styles["Justify"]))
    story.append(Spacer(1, 8))
    story.append(Spacer(1, 8))
    story.append(Spacer(1, 8))

    diploma_reg_number = '<font size=8 name=Verdana>%s %s</font>' % (reg_number, person_data['diploma_id'])
    story.append(Paragraph(diploma_reg_number, styles["Justify"]))
    story.append(Spacer(1, 8))
    
    doc.build(story)


if __name__ == '__main__':
    fname = raw_input('Введите путь к файлу с исходными данными: ')
    if not os.path.exists(fname):
        print('Файл %s не найден' % fname)
        exit()
    with open(fname) as f:
        reader = csv.DictReader(f, delimiter=',')
        for person_data in reader:
            build_diploma(person_data)
