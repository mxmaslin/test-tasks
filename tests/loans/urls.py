# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'partner_api/questionnaires', views.QuestionnaireViewSet)


urlpatterns = (

    # PartnerAPI
    url(r'^', include(router.urls)),
    url(r'^partner_api/make_submission/$', views.SubmissionCreate.as_view()),

    # BankAPI
    url(r'^submissions/$',
        views.BankAPI.as_view()),

    url(r'^submissions/(?P<pk>\S+)/$',
        views.BankAPI.get_submission)
)
