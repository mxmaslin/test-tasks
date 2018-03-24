# -*- coding: utf-8 -*-
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)


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
