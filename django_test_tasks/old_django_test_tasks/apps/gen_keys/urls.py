from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'gen_keys'

urlpatterns = [
    path('keys/', views.KeyList.as_view(), name='keys_list'),
    path('keys/<int:pk>/', views.KeyDetail.as_view(), name='key_detail'),
    path('keys/provide-key', views.provide_key, name='provide_key'),
]

urlpatterns = format_suffix_patterns(urlpatterns)