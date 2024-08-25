from rest_framework import serializers

from easy_xml.models import Product, Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['name', 'price',]


class ResultSerializer(serializers.ModelSerializer):
    end_at = serializers.DateField(source='promotion_end_date')
    base_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        source='tariff_base_price',
    )
    discount = serializers.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = serializers.SerializerMethodField()
    tariffs = TariffSerializer(many=True, source='tariff_set')

    class Meta:
        model = Product
        fields = [
            'name',
            'tariffs',
            'end_at',
            'base_price',
            'discount',
            'discounted_price',
        ]

    def get_discounted_price(self, obj):
        return obj.tariff_base_price - obj.discount
