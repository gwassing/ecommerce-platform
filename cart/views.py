from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import DeleteView, View

from . import models


class CartDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Cart
    template_name = 'cart/cart_detail.html'

    def get_object(self, queryset=None):
        obj = models.Cart.objects.get(pk=self.request.user.pk)
        return obj

    def get_context_data(self, **kwargs):
        cart_items = self.object.cart_items.all().select_related('product')
        total_price = sum((item.product.price * item.quantity) for item in cart_items)

        return super().get_context_data(**kwargs) | {
            "cart_items": cart_items,
            "total_items": cart_items.count(),
            "total_price": total_price
        }


class AddItemToCartView(View):
    model = models.CartItem

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        cart = models.Cart.objects.get(user=self.request.user)
        cart_item, created = models.CartItem.objects.get_or_create(product_id=product_id, cart=cart)

        if not created:
            cart_item.quantity += 1
            cart_item.save(update_fields=['quantity'])

        return redirect(reverse('cart:cart'))


class RemoveCartItemView(DeleteView):
    model = models.CartItem
    success_url = reverse_lazy('cart:cart')

    def get_queryset(self):
        # not strictly needed for functionality but good to do for security purposes
        return models.CartItem.objects.filter(cart__user=self.request.user)

