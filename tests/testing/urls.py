# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    # Question
    url(r'^questions/$', views.QuestionList.as_view()),
    url(r'^question/(?P<id>\d)/$', views.QuestionDetail.as_view()),

    # Answer
    url(r'^answers/$', views.AnswerList.as_view()),
    url(r'^answer/(?P<id>\d)/$', views.AnswerDetail.as_view()),

    # Test
    url(r'^tests/$', views.TestList.as_view()),
    url(r'^test/(?P<id>\d)/$', views.TestDetail.as_view()),

    # Author
    url(r'^authors/$', views.AuthorList.as_view()),
    url(r'^author/(?P<id>\w)/$', views.AuthorDetail.as_view()),

    # Respondent
    url(r'^respondents/$', views.RespondentList.as_view()),
    url(r'^respondent/(?P<id>\w)/$', views.RespondentDetail.as_view()),

    # Grade
    url(r'^grades/$', views.GradeList.as_view()),
    url(r'^grade/(?P<id>\d)/$', views.GradeDetail.as_view()),

]
