from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from products.models import Product
from cart.forms import AddItemToCartForm


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = "products"


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        context['cart_form'] = AddItemToCartForm()
        return context
