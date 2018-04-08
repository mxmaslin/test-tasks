# -*- coding: utf-8 -*-
from django.urls import include, path, re_path

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


urlpatterns = [

    # PartnerAPI
    re_path(r'^', include(router.urls)),
    path('partner_api/make_submission/', make_submission),

    # BankAPI
    path('bank_api/submissions/', submissions_list),
    re_path(r'bank_api/submissions/(?P<pk>[0-9]+)/', submission_detail)
]