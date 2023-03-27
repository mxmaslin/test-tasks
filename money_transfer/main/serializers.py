from rest_framework import serializers

from .models import PaymentUser


def validate_recipients(recipients):
    if len(recipients) != len(set(recipients)):
        raise serializers.ValidationError(
            'Дублирование получателей перевода не допускается'
        )
    return recipients


class PaymentUserSerializer(serializers.ModelSerializer):
    send_sum = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=0, required=True
    )
    recipients = serializers.ListField(
        child=serializers.CharField(
            max_length=10, min_length=10, allow_blank=False, required=True
        ),
        required=True,
        validators=[validate_recipients]
    )

    class Meta:
        model = PaymentUser
        fields = ['send_sum', 'recipients']
