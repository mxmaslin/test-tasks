# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'partner_api/questionnaires', views.QuestionnaireViewSet)


submissions_list = views.SubmissionViewSet.as_view({
    'get': 'list'})
submission_detail = views.SubmissionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'})
make_submission = views.SubmissionViewSet.as_view({
    'post': 'create'})


urlpatterns = (

    # PartnerAPI
    url(r'^', include(router.urls)),
    url(r'^partner_api/make_submission/$', make_submission),

    # BankAPI
    url(r'^bank_api/submissions/$',
        submissions_list),
    url(r'^bank_api/submissions/(?P<pk>[0-9]+)/$', submission_detail)
)
