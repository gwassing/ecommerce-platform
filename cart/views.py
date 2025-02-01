from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from . import models


class CartDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Cart
    template_name = 'cart/cart_detail.html'

    def get_object(self, queryset=None):
        obj = models.Cart.objects.get(pk=self.request.user.pk)
        return obj

    def get_context_data(self, **kwargs):
        cart_items = self.object.cart_items.all().select_related('product')
        total_price = sum(item.product.price for item in cart_items)

        return super().get_context_data(**kwargs) | {
            "cart_items": cart_items,
            "total_items": cart_items.count(),
            "total_price": total_price
        }
