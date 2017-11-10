# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Application
from .models import Questionnaire
from .models import Submission

from .serializers import ApplicationSerializer
from .serializers import QuestionnaireSerializer
from .serializers import SubmissionSerializer


class PartnerAPI(APIView):

    def get(self, request, format=None):
        '''
            Получение списка анкет
        '''
        questionnaires = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def get_by_pk(request, pk):
        '''
            Получение определённой анкеты
        '''
        try:
            questionnaire = Questionnaire.objects.get(pk=pk)
        except Questionnaire.DoesNotExist:
            raise Http404
        serializer = QuestionnaireSerializer(questionnaire)
        return Response(serializer.data)

    def post(self, request, format=None):
        '''
            Создание анкеты
        '''
        serializer = QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['POST'])
    def post_submission(request, format=None):
        '''
            Отправка заявки в кредитную организацию
        '''
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankAPI:

    @staticmethod
    @api_view(['GET'])
    def get_submissions(request):
        '''
            Получение списка заявок
        '''
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def get_submission(request, pk):
        '''
            Получение определённой заявки
        '''
        try:
            submission = Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            raise Http404
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)
