from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from products.models import Product


def index(request):
    return HttpResponse("hello world")


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

