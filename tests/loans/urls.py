# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = (

    # Предложения
    url(r'^applications/$',
        views.ApplicationList.as_view()),

    url(r'^applications/(?P<pk>\S+)/$',
        views.ApplicationDetail.as_view()),


    # Анкеты
    url(r'^questionnaires/$',
        views.QuestionnaireList.as_view()),

    url(r'^questionnaires/(?P<pk>\S+)/$',
        views.QuestionnaireDetail.as_view()),


    # Заявки
    url(r'^submissions/$',
        views.SubmissionList.as_view()),

    url(r'^submissions/(?P<pk>\S+)/$',
        views.SubmissionDetail.as_view())
)
