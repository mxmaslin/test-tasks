from django.urls import path

from easy_xml import views


urlpatterns = [
    path('products/', views.get_products),
]
