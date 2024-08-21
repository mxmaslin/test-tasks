from django.shortcuts import render
from django.http import HttpResponse


def xml_view(request):
    return HttpResponse("hi")
