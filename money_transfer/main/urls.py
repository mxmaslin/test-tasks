from django.urls import path

from . import views

urlpatterns = [
    path('<int:inn>/', views.MoneySender.as_view()),
]
