# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    # User
    url(r'^users/$', views.UserList.as_view()),
    url(r'^user/(?P<id>\d)/$', views.UserDetail.as_view()),

    # QuestionSet
    url(r'^questionsets/$', views.QuestionSetList.as_view()),
    url(r'^questionset/(?P<id>\d)/$', views.QuestionSetDetail.as_view()),

    # Question
    url(r'^questions/$', views.QuestionList.as_view()),
    url(r'^question/(?P<id>\d)/$', views.QuestionDetail.as_view()),

    # Option
    url(r'^options/$', views.OptionList.as_view()),
    url(r'^option/(?P<id>\w)/$', views.OptionDetail.as_view()),

    # Submission
    url(r'^submissions/$', views.SubmissionList.as_view()),
    url(r'^submission/(?P<id>\w)/$', views.SubmissionDetail.as_view()),

]
