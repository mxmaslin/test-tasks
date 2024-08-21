from django.urls import path

from easy_xml import views


urlpatterns = [
    path('test', views.xml_view),
]
