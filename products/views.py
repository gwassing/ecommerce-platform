from django.views.generic import DetailView, ListView, TemplateView

from products.models import Product


class IndexView(TemplateView):
    template_name = "products/index.html"


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

