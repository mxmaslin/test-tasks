from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .models import QuestionSet
from .models import Question
from .models import Option
from .models import Submission

from .serializers import UserSerializer
from .serializers import QuestionSetSerializer
from .serializers import QuestionSerializer
from .serializers import OptionSerializer
from .serializers import SubmissionSerializer

#############################################################
# <User>


class UserList(APIView):
    '''
        List all users, or create a new user
    '''
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    '''
        Retrieve, update or delete an user instance
    '''
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# </User>
#############################################################
# <QuestionSet>


class QuestionSetList(APIView):
    """
        List all questionsets, or create a new question sets
    """
    def get(self, request, format=None):
        question_sets = QuestionSet.objects.all()
        serializer = QuestionSetSerializer(question_sets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionSetDetail(APIView):
    """
        Retrieve, update or delete a question set instance
    """
    def get_object(self, pk):
        try:
            return QuestionSet.objects.get(pk=pk)
        except QuestionSet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question_set = self.get_object(pk)
        serializer = QuestionSetSerializer(question_set)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        question_set = self.get_object(pk)
        serializer = QuestionSetSerializer(question_set, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question_set = self.get_object(pk)
        question_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# </QuestionSet>
#############################################################
# <Question>


class QuestionList(APIView):
    '''
        List all questions, or create a new question
    '''
    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    '''
        Retrieve, update or delete a question instance
    '''
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# </Question>
#############################################################
# <Option>


class OptionList(APIView):
    '''
        List all options, or create a new option
    '''
    def get(self, request, format=None):
        options = Option.objects.all()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OptionDetail(APIView):
    '''
        Retrieve, update or delete an option instance.
    '''
    def get_object(self, pk):
        try:
            return Option.objects.get(pk=pk)
        except Option.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        option = self.get_object(pk)
        serializer = OptionSerializer(option)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        option = self.get_object(pk)
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        option = self.get_object(pk)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# </Option>
#############################################################
# <Submission>


class SubmissionList(APIView):
    '''
        List all submissions, or create a new submission
    '''
    def get(self, request, format=None):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionDetail(APIView):
    '''
        Retrieve, update or delete a submission instance.
    '''
    def get_object(self, pk):
        try:
            return Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        submission = self.get_object(pk)
        serializer = RespondentSerializer(submission)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        submission = self.get_object(pk)
        serializer = SubmissionSerializer(submission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        submission = self.get_object(pk)
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# </Submission>
#############################################################
