# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'questionnaires', views.PartnerAPI)

# make_submission = views.PartnerAPI.as_view({
#     'post': 'make_submission'})

urlpatterns = (

    # PartnerAPI
    url(r'^', include(router.urls)),
    # url(r'^make_submission/$', make_submission),





    # url(r'^questionnaires/submit/$',
    #     views.PartnerAPI.submit),

    # url(r'^questionnaires/$',
    #     views.PartnerAPI.as_view()),

    # url(r'^questionnaires/(?P<pk>\S+)/$',
    #     views.PartnerAPI.get_by_pk),


    # BankAPI

    url(r'^submissions/$',
        views.BankAPI.as_view()),

    url(r'^submissions/(?P<pk>\S+)/$',
        views.BankAPI.get_submission)
)
