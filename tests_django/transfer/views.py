# -*- coding: utf-8 -*-
import string
from django.http import HttpResponse
from django.shortcuts import render

from .forms import SendMoneyForm
from .models import Client


def index(request):
    form = SendMoneyForm(request.POST or None)
    if form.is_valid():
        donor = form.cleaned_data['donor']
        recipients_string = form.cleaned_data['recipients']
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        recipient_inns = list(map(int, recipients_string.translate(translator).split()))
        recipients = Client.objects.filter(inn__in=recipient_inns)
        amount = form.cleaned_data['amount']
        donor.balance -= amount
        donor.save()
        payment_for_each_recipient = amount / len(recipients)
        for recipient in recipients:
            recipient.balance += payment_for_each_recipient
            recipient.save()
        return HttpResponse('thanks')
    return render(request, 'transfer/index.html', {'form': form})
