from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView

from . import models, forms
from products import models as product_models


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


class CreateCartItemView(CreateView):
    model = models.CartItem
    form_class = forms.CreateCartItemForm
    success_url = reverse_lazy('cart:cart')

    def form_valid(self, form):
        cart_item = form.save(commit=False)
        cart_item.product = get_object_or_404(product_models.Product, id=self.kwargs.get('product_id'))
        cart_item.cart = models.Cart.objects.get(user=self.request.user)

        cart_item.save()

        return super().form_valid(form)


class RemoveCartItemView(DeleteView):
    model = models.CartItem
    success_url = reverse_lazy('cart:cart')

    def get_queryset(self):
        # not strictly needed for functionality but good to do for security purposes
        return models.CartItem.objects.filter(cart__user=self.request.user)

