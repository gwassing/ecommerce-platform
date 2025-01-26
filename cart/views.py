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
        return super().get_context_data(**kwargs) | {
            "cart_items": self.object.cartitem_set.all(),
            "total_items": self.object.cartitem_set.all().count()
        }
