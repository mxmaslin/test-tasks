# -*- coding: utf-8 -*-
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)


where = {
    'where': 'ГАОУ ДПО ЦПМ'}

when = {
    'when_begin_day': '15',
    'when_begin_month': 'сентября',
    'when_begin_year': '2014',
    'when_end_day': '30',
    'when_end_month': 'июня',
    'when_end_year': '2015'}

guys = {
    'director': 'И.В. Ященко',
    'some_boss': 'А.А. Якута'}

program = 'по дополнительной профессиональной программе<br />\
«Развитие таланта школьников в предметных областях.<br />\
Организация и проведение этапов всероссийской олимпиады<br />\
школьников и других интеллектуальных соревнований»'

module = 'модуль «Особенности применения технологии<br />\
музейной педагогики в развитии детской одарённости.<br />\
Олимпиада "Музеи. Парки. Усадьбы"»'

volume = 'в объёме 24 (двадцати четырёх) часов'

director = 'М.П. &nbsp;&nbsp;&nbsp;&nbsp;\
Директор &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
%(director)s' % guys
some_boss = 'Начальник<br />\
учебной части &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; %(some_boss)s' % guys

city = 'Москва, 2015'

diploma_info = 'Удостоверение является документом<br />\
установленного образца'

reg_number = 'Регистрационный номер'


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Arial',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Arial',
            bulletFontSize=8,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['person_name'] = ParagraphStyle(
        'diploma_info',
        parent=styles['default'],
        fontName='Arial-Bold',
    )
    styles['some_boss'] = ParagraphStyle(
        'diploma_info',
        parent=styles['default'],
        alignment=TA_LEFT
    )
    return styles

