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

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Это поле не может иметь отрицательное значение')
        return amount
