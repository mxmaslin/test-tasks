# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

from .forms import SendMoneyForm


def index(request):
    form = SendMoneyForm(request.POST or None)
    if form.is_valid():
        donor = form.cleaned_data['donor']
        recipients = form.cleaned_data['recipients']
        amount = form.cleaned_data['amount']

        return HttpResponse('thanks')
    return render(request, 'transfer/index.html', {'form': form})
