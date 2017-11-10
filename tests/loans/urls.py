# -*- coding: utf-8 -*-
"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = (

    # Предложения
    url(r'^applications/$',
        views.ApplicationListView.as_view(),
        name='applications_list'),

    url(r'^applications/create/$',
        views.ApplicationCreateView.as_view(),
        name='applications_create'),

    url(r'^applications/detail/(?P<pk>\S+)/$',
        views.ApplicationDetailView.as_view(),
        name='applications_detail'),

    url(r'^applications/update/(?P<pk>\S+)/$',
        views.ApplicationUpdateView.as_view(),
        name='applications_update'),


    # Анкеты
    url(r'^questionnaires/$',
        views.QuestionnaireListView.as_view(),
        name='questionnaires_list'),

    url(r'^questionnaires/create/$',
        views.QuestionnaireCreateView.as_view(),
        name='questionnaires_create'),

    url(r'^questionnaires/detail/(?P<pk>\S+)/$',
        views.QuestionnaireDetailView.as_view(),
        name='questionnaires_detail'),

    url(r'^questionnaires/update/(?P<pk>\S+)/$',
        views.QuestionnaireUpdateView.as_view(),
        name='questionnaires_update')

    # Заявки
    url(r'^submissions/$',
        views.SubmissionListView.as_view(),
        name='submission_list'),

    url(r'^submissions/create/$',
        views.SubmissionCreateView.as_view(),
        name='submission_create'),

    url(r'^submission/detail/(?P<pk>\S+)/$',
        views.SubmissionDetailView.as_view(),
        name='submission_detail'),

    url(r'^submission/update/(?P<pk>\S+)/$',
        views.SubmissionUpdateView.as_view(),
        name='submission_update'),

)
