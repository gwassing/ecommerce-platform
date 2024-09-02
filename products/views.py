from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from products.models import Product


def index(request):
    return HttpResponse("hello world")


def product_list(request):
    return HttpResponse("list of products")


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return HttpResponse(f"This is {product.item_name} with product id {product.id}.")
