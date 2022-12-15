# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views

app_name = 'image_sizer_app'

urlpatterns = [
    re_path(r'^$', views.image_create),
    re_path(
        r'^(?P<slug>media\/images\/\d{4}\/\d{2}\/\d{2}\/[a-zA-Z0-9_-]+(.jpg|.JPG|.gif|.GIF|.png|.PNG)*)$',
        views.ResizeDetail.as_view(),
        name='resize_detail')
]
