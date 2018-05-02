from django.shortcuts import render

from django.http import HttpResponse


def index(request, download_url):
    return HttpResponse("url is %s" % download_url)
