# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.image_create),
    re_path(
        r'(?P<path>)/',
        views.ResizeDetail.as_view(), name='resize-detail')
]
