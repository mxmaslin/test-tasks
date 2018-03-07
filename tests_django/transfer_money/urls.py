from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SendMoneyFormView.as_view())
]
