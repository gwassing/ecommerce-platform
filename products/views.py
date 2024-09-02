from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from products.models import Product


def index(request):
    return HttpResponse("hello world")


def product_list(request):
    return HttpResponse("list of products")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
