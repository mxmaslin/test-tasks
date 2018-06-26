# -*- coding: utf-8 -*-
from django.urls import path, re_path

from . import views


urlpatterns = [

    # Создать ребёнка
    re_path(r'^children/$', views.child_create),

    # Создать отметку в журнал
    re_path(r'^records/$', views.record_list),
    # Изменить отметку в журнале
    path('records/<int:pk>/', views.record_detail),
    # Список тех, кто сейчас учится
    path('records/studying/', views.record_studying)
]
