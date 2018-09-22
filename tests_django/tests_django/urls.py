# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),

    path('loans/', include('loans.urls')),
    path('menu-tag/', include('menu_tag.urls')),
    path('testing/', include('testing.urls')),
    path('transfer-money/', include('transfer_money.urls')),
    # path('image-sizer/',
    #      include('image_sizer.urls', namespace='image_sizer_app')),
    path('playschool/', include('playschool.urls')),
    path('cars/', include('cars.urls')),
    path('cats/', include('cats.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
