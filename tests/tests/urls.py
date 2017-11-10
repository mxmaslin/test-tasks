# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^testing/', include('testing.urls')),
    url(r'^api/loans/', include('loans.urls')),

    url(r'^admin/', admin.site.urls)
]
