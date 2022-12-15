from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('cats/', include('apps.cats.urls')),
    path('cars/', include('apps.cars.urls')),
    # path('image-sizer/', include('apps.image_sizer.urls')),
    path('loans/', include('apps.loans.urls')),
    path('menu-tag/', include('apps.menu_tag.urls')),
    path('playschool/', include('apps.playschool.urls')),
    # path('testing/', include('apps.testing.urls')),
    path('transfer-money/', include('apps.transfer_money.urls')),
    path('generate-keys/', include('apps.gen_keys.urls')),
    path('blog/', include('apps.blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
