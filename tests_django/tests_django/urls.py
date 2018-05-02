# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),

    path('loans/', include('loans.urls')),
    path('menu-tag/', include('menu_tag.urls')),
    path('testing/', include('testing.urls')),
    path('transfer-money/', include('transfer_money.urls')),
    path('image-sizer/', include('image_sizer.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
