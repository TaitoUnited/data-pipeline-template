from django.http.response import JsonResponse
import typing
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from src.app.config import Config
from src.common.utils.validate import validate_api_key

from .models import Sales
from .serializers import SaleSerializer, SaleCreateSerializer


@api_view(["GET", "POST", "DELETE"])
def sales(request) -> typing.Any:
    # Authorize
    validate_api_key(request, Config.API_KEY)

    if request.method == "GET":
        sales = Sales.objects.all()

        title = request.query_params.get("title", None)
        if title is not None:
            sales = sales.filter(title__icontains=title)

        sales_serializer = SaleSerializer(sales, many=True)
        return JsonResponse(sales_serializer.data, safe=False)

    elif request.method == "POST":
        sale_data = JSONParser().parse(request)
        sales_create_serializer = SaleCreateSerializer(data=sale_data)
        if sales_create_serializer.is_valid():
            sales_create_serializer.save()
            return JsonResponse(
                sales_create_serializer.data, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            sales_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        count = Sales.objects.all().delete()
        return JsonResponse(
            {
                "message": "{} Sales were deleted successfully!".format(
                    count[0]
                )
            },
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def sale(request, id) -> typing.Any:
    # Authorize
    validate_api_key(request, Config.API_KEY)

    try:
        sale = Sales.objects.get(pk=id)
    except Sales.DoesNotExist:
        return JsonResponse(
            {"message": "The sale does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        sale_serializer = SaleSerializer(sale)
        return JsonResponse(sale_serializer.data)

    elif request.method == "PUT":
        sale_data = JSONParser().parse(request)
        sale_serializer = SaleCreateSerializer(
            sale, data=sale_data, partial=True
        )
        print(sale_serializer)
        if sale_serializer.is_valid():
            sale_serializer.save()
            return JsonResponse(sale_serializer.data)
        return JsonResponse(
            sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        sale.delete()
        return JsonResponse(
            {"message": "Sale was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )
