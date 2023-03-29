from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'send/<int:inn>/', views.MoneySender.as_view(), name='money_transfer'
    ),
]
