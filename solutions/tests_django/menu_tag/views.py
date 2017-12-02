# -*- coding: utf-8 -*-
from django.shortcuts import render


def index(request):
    '''
        http://127.0.0.1:8000/menu_tag/?item=abc
        abc это slug пункта меню
    '''
    return render(request, 'menu_tag/index.html')
