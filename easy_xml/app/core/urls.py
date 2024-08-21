from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('easy-xml/', include('easy_xml.urls')),
]
