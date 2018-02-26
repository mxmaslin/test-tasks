import string

from django import forms
from djmoney.forms import MoneyWidget
from djmoney.models.fields import MoneyField

from .models import Client


class SendMoneyForm(forms.Form):
    donor = forms.ModelMultipleChoiceField(queryset=Client.objects.all())
    recipients = forms.CharField(widget=forms.TextInput)
    amount = MoneyField(widget=MoneyWidget)

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        inns = data.translate(translator).split()
        clients_inn_list = Client.objects.all().values_list('inn', flat=True)
        for inn in inns:
            if inn not in clients_inn_list:
                raise forms.ValidationError('Инн {} отсутствует в базе данных'.format(inn))
        return data

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Это поле не может иметь отрицательное значение')
        return amount
