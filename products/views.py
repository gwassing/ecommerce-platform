from django.core.cache import cache
from django.views.generic import DetailView, ListView, TemplateView

from products.models import Product
from cart.forms import AddItemToCartForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        context['cart_form'] = AddItemToCartForm()
        return context


class BrandsListView(TemplateView):
    template_name = 'products/brands_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
        return context
