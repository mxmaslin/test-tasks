from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from easy_xml.models import Product, Tariff, Promotion
from easy_xml.serializers import ProductSerializer, TariffSerializer, PromotionSerializer


@csrf_exempt
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)
