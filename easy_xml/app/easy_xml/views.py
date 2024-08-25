from django.db.models import OuterRef, Subquery

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from easy_xml.models import Product, Promotion
from easy_xml.serializers import ResultSerializer


@api_view(['GET'])
@renderer_classes([XMLRenderer])
def get_products(request):
    max_discount_promotion_subquery = (
        Promotion.objects
        .filter(tariffs__product=OuterRef('pk'))
        .order_by('-discount')
        .values('id')[:1]
    )

    max_discount_promotion_tariff_subquery = (
        Promotion.objects
        .filter(tariffs__product=OuterRef('pk'))
        .order_by('-discount')
        .values('tariffs__id')[:1]
    )

    promotion_end_at_subquery = (
        Promotion.objects
        .filter(tariffs__product=OuterRef('pk'))
        .order_by('-discount')
        .values('end_at')[:1]
    )
    tariff_base_price_subquery = (
        Promotion.objects
        .filter(tariffs__product=OuterRef('pk'))
        .order_by('-discount')
        .values('tariffs__price')[:1]
    )
    discount_subquery = (
        Promotion.objects
        .filter(tariffs__product=OuterRef('pk'))
        .order_by('-discount')
        .values('discount')[:1]
    )

    products_with_tariffs_and_promotion = (
        Product.objects
        .annotate(
            max_discount_promotion=Subquery(max_discount_promotion_subquery),
            max_discount_promotion_tariff=Subquery(
                max_discount_promotion_tariff_subquery
            ),

            promotion_end_date=Subquery(promotion_end_at_subquery),
            tariff_base_price=Subquery(tariff_base_price_subquery),
            discount=Subquery(discount_subquery),
        )
        .prefetch_related('tariff_set__promotion_set')
    )
    serializer = ResultSerializer(
        products_with_tariffs_and_promotion, many=True
    )
    return Response(serializer.data)
