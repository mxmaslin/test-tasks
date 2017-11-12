# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import (
    Application,
    Questionnaire,
    Submission)

from .serializers import (
    ApplicationSerializer,
    QuestionnaireSerializer,
    SubmissionSerializer)

# from rest_framework.filters import OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# from rest_framework.filters import OrderingFilter


class PartnerAPI(generics.ListAPIView):

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'phone', 'passport')
    # ordering_fields = ('created', 'modified', 'birthday', 'score')


# class PartnerAPI(APIView):

#     filter_backends = (SearchFilter,)
#     search_fields = ('name', 'phone', 'passport')
#     ordering_fields = ('created', 'modified', 'birthday', 'score')

#     def get(self, request, format=None):
#         '''
#             Получение списка анкет
#             http GET http://127.0.0.1:8000/api/loans/questionnaires/

#             Поиск среди анкет по критерию:
#             - name: http GET http://127.0.0.1:8000/api/loans/questionnaires/?search=Иван
#             - phone: http GET http://127.0.0.1:8000/api/loans/questionnaires/?search=123
#             - passport: http GET http://127.0.0.1:8000/api/loans/questionnaires/

#             Получение отсортированного списка анкет по критерию:
#             - created: http GET http://127.0.0.1:8000/api/loans/questionnaires/
#             - modified: http GET http://127.0.0.1:8000/api/loans/questionnaires/
#             - birthday: http GET http://127.0.0.1:8000/api/loans/questionnaires/
#             - score: http GET http://127.0.0.1:8000/api/loans/questionnaires/
#         '''
#         questionnaires = Questionnaire.objects.all()
#         serializer = QuestionnaireSerializer(questionnaires, many=True)
#         return Response(serializer.data)

#     @staticmethod
#     @api_view(['GET'])
#     def get_by_pk(request, pk):
#         '''
#             Получение определённой анкеты
#             http GET http://127.0.0.1:8000/api/loans/questionnaires/1/
#         '''
#         try:
#             questionnaire = Questionnaire.objects.get(pk=pk)
#         except Questionnaire.DoesNotExist:
#             raise Http404
#         serializer = QuestionnaireSerializer(questionnaire)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         '''
#             Создание анкеты
#             http POST http://127.0.0.1:8000/api/loans/questionnaires/ <<< '{"name": "Давид Соломонович", "birthday": "2017-05-30", "passport": "abc123", "phone": "130-19-32", "score": 5}'
#         '''
#         serializer = QuestionnaireSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @staticmethod
#     @api_view(['POST'])
#     def submit(request, format=None):
#         '''
#             Отправка заявки в кредитную организацию
#             http POST http://127.0.0.1:8000/api/loans/questionnaires/submit/ <<< '{"application": 1, "questionnaire": 1, "status": 1, "created": "2017-11-10T18:23:16.913526Z", "submitted": "2017-11-10T18:23:16.913526Z"}'
#         '''
#         serializer = SubmissionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankAPI:

    filter_fields = ('status',)
    search_fields = ('application', 'questionnaire')
    ordering_fields = ('created', 'submitted')

    @staticmethod
    @api_view(['GET'])
    def get_submissions(request):
        '''
            Получение списка заявок
            http GET http://127.0.0.1:8000/api/loans/submissions/

            Получение отфильтрованного списка заявок по критерию:
            - status: http GET http://127.0.0.1:8000/api/loans/submissions/

            Поиск среди заявок по критерию:
            - application: http GET http://127.0.0.1:8000/api/loans/submissions/
            - questionnaire: http GET http://127.0.0.1:8000/api/loans/submissions/

            Получение отсортированного списка анкет по критерию:
            - created: http GET http://127.0.0.1:8000/api/loans/submissions/
            - submitted: http GET http://127.0.0.1:8000/api/loans/submissions/
        '''
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def get_submission(request, pk):
        '''
            Получение определённой заявки
            http GET http://127.0.0.1:8000/api/loans/submissions/1/
        '''
        try:
            submission = Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            raise Http404
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)
