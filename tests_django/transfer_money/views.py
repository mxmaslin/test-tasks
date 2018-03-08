# -*- coding: utf-8 -*-
import string
from django.http import JsonResponse
from django.views.generic.edit import FormView

from .forms import SendMoneyForm
from .models import Client


class SendMoneyFormView(FormView):
    form_class = SendMoneyForm
    template_name = 'transfer_money/index.html'
    success_url = 'transfer_money/index.html'

    def get(self, request, *args, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        # context['form'] = form
        context['clients'] = Client.objects.all()
        return self.render_to_response(context)

    def form_invalid(self, form):
        response = super(SendMoneyFormView, self).form_invalid(form)
        if self.request.is_ajax():
            # print(form.errors)
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
            amount = form.cleaned_data['amount']
            donor.balance -= amount
            donor.save()
            payment_for_each_recipient = amount / len(recipients)
            for recipient in recipients:
                recipient.balance += payment_for_each_recipient
                recipient.save()
            clients = list(Client.objects.values())
            data = {'message': 'Форма успешно отправлена',
                    'clients': clients}
            return JsonResponse(data)
        else:
            return response
