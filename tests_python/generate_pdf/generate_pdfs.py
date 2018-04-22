# -*- coding: utf-8 -*-
import os
import csv

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


from reportlab.graphics import renderPDF

from diploma_content import (where,
                             when,
                             program,
                             module,
                             volume,
                             director,
                             some_boss,
                             city,
                             diploma_info,
                             reg_number)

from styles import stylesheet


pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial Bold.ttf'))


def build_diploma_number(i, num_diploma_digits, last_diploma_numer):
    num_digits_i = len(str(i))
    padding = '0' * (num_diploma_digits - num_digits_i)
    return str(i) if i == last_diploma_numer else padding + str(i)


def build_diploma(person_data, diploma_number):
    diploma_fname = 'diplom%s.pdf' % diploma_number
    path_to_diploma = os.path.join('diplomas', diploma_fname)

    c = canvas.Canvas(path_to_diploma, pagesize=landscape(A4), bottomup=0)

    person_text = '%(family)s %(name)s %(patronymic)s' % person_data
    person_para = Paragraph(person_text, stylesheet()['person_name'])
    person_para.wrapOn(c, 200, 10)
    person_para.drawOn(c, 500, 200)

    where_text = 'прошел(а) обучение в %(where)s' % where
    where_para = Paragraph(where_text, stylesheet()['default'])
    where_para.wrapOn(c, 200, 10)
    where_para.drawOn(c, 499, 225)

    when_text = 'c «%(when_begin_day)s» %(when_begin_month)s %(when_begin_year)s \
    по «%(when_end_day)s» %(when_end_month)s %(when_end_year)s' % when
    when_para = Paragraph(when_text, stylesheet()['default'])
    when_para.wrapOn(c, 200, 10)
    when_para.drawOn(c, 499, 240)

    program_para = Paragraph(program, stylesheet()['default'])
    program_para.wrapOn(c, 300, 10)
    program_para.drawOn(c, 450, 230)

    module_para = Paragraph(module, stylesheet()['default'])
    module_para.wrapOn(c, 300, 10)
    module_para.drawOn(c, 450, 305)

    volume_para = Paragraph(volume, stylesheet()['default'])
    volume_para.wrapOn(c, 200, 10)
    volume_para.drawOn(c, 500, 380)

    director_para = Paragraph(director, stylesheet()['default'])
    director_para.wrapOn(c, 300, 10)
    director_para.drawOn(c, 450, 420)

    some_boss_para = Paragraph(some_boss, stylesheet()['some_boss'])
    some_boss_para.wrapOn(c, 300, 10)
    some_boss_para.drawOn(c, 543, 435)

    city_para = Paragraph(city, stylesheet()['default'])
    city_para.wrapOn(c, 100, 10)
    city_para.drawOn(c, 555, 490)

    diploma_info_para = Paragraph(diploma_info, stylesheet()['default'])
    diploma_info_para.wrapOn(c, 300, 10)
    diploma_info_para.drawOn(c, 50, 410)

    reg_number_full = '%s %s' % (reg_number, diploma_number)
    reg_number_para = Paragraph(reg_number_full, stylesheet()['default'])
    reg_number_para.wrapOn(c, 300, 10)
    reg_number_para.drawOn(c, 28, 480)

    qrw = QrCodeWidget(diploma_number)
    dr = Drawing(45, 45)
    dr.add(qrw)
    renderPDF.draw(dr, c, 101, 485)

    c.save()


if __name__ == '__main__':
    # fname = raw_input('Введите путь к файлу с исходными данными: ')
    fname = 'persons.csv'
    if not os.path.exists(fname):
        print('Файл %s не найден' % fname)
        exit()
    with open(fname) as f:
        last_diploma_numer = len(open(fname).readlines())
        num_diploma_digits = len(str(last_diploma_numer))

        reader = csv.DictReader(f, delimiter=',')

        for i, person_data in enumerate(reader, start=1):
            diploma_number = build_diploma_number(i, num_diploma_digits, last_diploma_numer)
            build_diploma(person_data, diploma_number)
