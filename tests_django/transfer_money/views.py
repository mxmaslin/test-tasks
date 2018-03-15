# -*- coding: utf-8 -*-
import string

from django.db import transaction
from django.http import JsonResponse
from django.views.generic.edit import FormView

from djmoney.money import Money

from .forms import SendMoneyForm
from .models import Client


class SendMoneyFormView(FormView):
    form_class = SendMoneyForm
    template_name = 'transfer_money/index.html'
    success_url = 'transfer_money/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        return self.render_to_response(context)

    def form_invalid(self, form):
        response = super(SendMoneyFormView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=500)
        else:
            return response

    def form_valid(self, form):
        response = super(SendMoneyFormView, self).form_valid(form)
        if self.request.is_ajax():
            donor = form.cleaned_data['donor']
            recipients_string = form.cleaned_data['recipients']
            translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
            recipient_inns = list(map(int, recipients_string.translate(translator).split()))
            recipients = Client.objects.filter(inn__in=recipient_inns)

            with transaction.atomic():
                amount = form.cleaned_data['amount']
                payment_for_each_recipient = amount / recipients.count()
                correct_payment_for_each_recipient = Money(round(float(payment_for_each_recipient) - 0.005, 2), 'RUB')
                actual_payment = Money(
                    round(float(payment_for_each_recipient), 2) * recipients.count(), 'RUB')
                correction_amount = Money(0.01, 'RUB') if actual_payment != amount else Money(0, 'RUB')
                donor.balance += correction_amount
                donor.balance -= amount
                donor.save()
                for recipient in recipients:
                    recipient.balance += correct_payment_for_each_recipient
                    recipient.save()
            clients = list(Client.objects.values())
            data = {'message': 'Форма успешно отправлена',
                    'clients': clients}
            return JsonResponse(data)
        else:
            return response
