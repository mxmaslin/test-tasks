import string
from decimal import Decimal

from django import forms
from djmoney.forms.fields import MoneyField

from .models import Client


class SendMoneyForm(forms.Form):
    donor = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(), label='Отправитель')
    recipients = forms.CharField(widget=forms.Textarea, label='Получатели')
    amount = MoneyField(label='Сумма')

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        inns = data.translate(translator).split()
        clients_inn_list = Client.objects.all().values_list('inn', flat=True)
        for inn in inns:
            if int(inn) not in clients_inn_list:
                raise forms.ValidationError('Инн {} отсутствует в базе данных'.format(inn))
        return data

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount.amount < 0.01:
            raise forms.ValidationError('Это поле не может быть меньше 0.01')
        donor_id = self.cleaned_data['donor'].split()[0]
        donor = Client.objects.get(id=donor_id)
        if amount > donor.balance:
            raise forms.ValidationError('Сумма превышает баланс отправителя')
        return amount
