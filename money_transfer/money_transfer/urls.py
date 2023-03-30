from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'send/', views.MoneySender.as_view(), name='send'
    ),
]
