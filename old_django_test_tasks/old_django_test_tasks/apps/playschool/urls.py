# -*- coding: utf-8 -*-
from django.urls import path, re_path

from . import views


urlpatterns = [

    # Создать ребёнка
    re_path(r'^scholars/$', views.ScholarCreateAPIView.as_view()),

    # Создать отметку в журнал
    re_path(r'^records/$', views.RecordCreateAPIView.as_view()),
    # Изменить отметку в журнале
    path('records/<int:pk>/', views.RecordUpdateAPIView.as_view()),
    # Список тех, кто сейчас учится
    path('records/studying/', views.studying_scholars_records)
]
