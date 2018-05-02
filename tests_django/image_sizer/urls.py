# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.image_create),
    re_path(
        r'(?P<download_url>(?:[-\w.]|(?:%[\da-fA-F]{2}))+)/',
        views.ResizeDetail.as_view())
]
