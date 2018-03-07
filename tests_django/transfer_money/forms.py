import string
from decimal import Decimal

from django import forms
from djmoney.forms.fields import MoneyField

from .models import Client


class SendMoneyForm(forms.Form):
    donor = forms.ModelChoiceField(
        queryset=Client.objects.all(), label='Отправитель')
    recipients = forms.CharField(widget=forms.Textarea, label='Получатели')
    amount = MoneyField(label='Сумма')

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        inns = data.translate(translator).split()
        clients_inn_list = Client.objects.all().values_list('inn', flat=True)
        errors = []
        non_digit_inns = []
        absent_inns = []
        for inn in inns:
            try:
                int_inn = int(inn)
            except ValueError:
                if inn not in non_digit_inns:
                    non_digit_inns.append(inn)
            else:
                if int_inn not in clients_inn_list:
                    if str(int_inn) not in absent_inns:
                        absent_inns.append(str(int_inn))
        for inn in non_digit_inns:
            errors.append('Инн {} должен состоять только из цифр'.format(inn))
        for inn in absent_inns:
            errors.append('Инн {} отсутствует в базе данных'.format(inn))
        if errors:
            raise forms.ValidationError(errors)
        return data

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        donor = self.cleaned_data['donor']
        if amount.amount < 0.01:
            raise forms.ValidationError('Это поле не может быть меньше 0.01')
        if amount > donor.balance:
            raise forms.ValidationError('Сумма превышает баланс отправителя')
        return amount
