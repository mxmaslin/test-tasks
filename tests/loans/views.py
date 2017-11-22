# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from dry_rest_permissions.generics import DRYPermissions

from .models import (
    Application,
    Questionnaire,
    Submission)

from .serializers import (
    ApplicationSerializer,
    QuestionnaireSerializer,
    SubmissionSerializer,
    SubmissionSerializerPost)


class QuestionnaireViewSet(viewsets.ModelViewSet):

    permission_classes = (DRYPermissions,)
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    search_fields = (
        'name',
        'phone',
        'passport')
    ordering_fields = (
        'created',
        'modified',
        'birthday',
        'score')


class SubmissionViewSet(viewsets.ModelViewSet):

    permission_classes = (DRYPermissions,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_fields = ('status',)
    search_fields = ('application__application_name', 'questionnaire__name')
    ordering_fields = ('created', 'submitted')

    # def create(self, request, *args, **kwargs):
    #     serializer = SubmissionSerializerPost(
    #         data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED,
    #         headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.groups.filter(name='Кредитные организации').exists():
            instance.status = 2
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
