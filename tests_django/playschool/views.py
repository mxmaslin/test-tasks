from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import Scholar, Record
from .serializers import ScholarSerializer, RecordSerializer


class ScholarCreateAPIView(CreateAPIView):
    queryset = Scholar.objects.all()
    serializer_class = ScholarSerializer


class RecordCreateAPIView(CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class RecordUpdateAPIView(UpdateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


@api_view(['GET'])
def studying_scholars_records(request):
    are_studying = Record.studying.all()
    serializer = RecordSerializer(are_studying, many=True)
    return Response(serializer.data)
