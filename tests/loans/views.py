# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import (
    Application,
    Questionnaire,
    Submission)

from .serializers import (
    ApplicationSerializer,
    QuestionnaireSerializer,
    SubmissionSerializer,
    SubmissionSerializerPost)


class PartnerAPI(generics.ListCreateAPIView):

    '''
        Получение списка всех анкет
        http GET http://127.0.0.1:8000/api/loans/questionnaires/

        Поиск среди анкет по одному из критериев (name, phone, passport):
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?search=Иван
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?search=123
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?search=abc

        Получение отсортированного списка анкет по одному из критериев (created, modified, birthday, score):
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?ordering=created
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?ordering=modified
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?ordering=birthday
        http GET http://127.0.0.1:8000/api/loans/questionnaires/?ordering=score

        Создание анкеты
        http POST http://127.0.0.1:8000/api/loans/questionnaires/ <<< '{"name": "Давид Соломонович", "birthday": "2017-05-30", "passport": "abc123", "phone": "130-19-32", "score": 5}'

        Получение определённой анкеты
        http GET http://127.0.0.1:8000/api/loans/questionnaires/1/

        Отправка заявки в кредитную организацию
        http POST http://127.0.0.1:8000/api/loans/questionnaires/submit/ <<< '{"application": 2, "questionnaire": 1, "status": 1, "created": "2017-11-10T18:23:16.913526Z", "submitted": "2017-11-10T18:23:16.913526Z"}'
    '''

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    search_fields = ('name', 'phone', 'passport')
    ordering_fields = ('created', 'modified', 'birthday', 'score')

    @staticmethod
    @api_view(['GET'])
    def get_by_pk(request, pk):
        try:
            questionnaire = Questionnaire.objects.get(pk=pk)
        except Questionnaire.DoesNotExist:
            raise Http404
        serializer = QuestionnaireSerializer(questionnaire)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def submit(request):
        serializer = SubmissionSerializerPost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankAPI(generics.ListAPIView):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_fields = ('status',)
    search_fields = ('application__application_name', 'questionnaire__name')
    ordering_fields = ('created', 'submitted')

    '''
        Получение списка всех заявок
        http GET http://127.0.0.1:8000/api/loans/submissions/

        Получение отфильтрованного списка заявок по критерию:
        http GET http://127.0.0.1:8000/api/loans/submissions/?status=0

        Поиск среди заявок по одному из критериев (application, questionnaire):
        http GET http://127.0.0.1:8000/api/loans/submissions/?=Моё

        Получение отсортированного списка анкет по одному из критериев (created, submitted):
        http GET http://127.0.0.1:8000/api/loans/submissions/?ordering=created

        Получение определённой заявки
        http GET http://127.0.0.1:8000/api/loans/submissions/3/
    '''

    @staticmethod
    @api_view(['GET'])
    def get_submission(request, pk):
        try:
            submission = Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            raise Http404
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)
