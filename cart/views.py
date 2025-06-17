import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from . import models, forms

logger = logging.getLogger('ecommerce-platform')


class CartDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Cart
    template_name = 'cart/cart_detail.html'

    def get_object(self, queryset=None):
        obj = models.Cart.objects.get(user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):

        return super().get_context_data(**kwargs) | {
            "cart_items": self.object.get_cart_items(),
            "total_items": self.object.get_cart_items().count(),
            "total_price": self.object.get_total_cart_price(),
            "cart_is_empty": self.object.get_cart_items().count() == 0
        }


class AddItemToCartView(generic.View):
    model = models.CartItem

    def post(self, request, *args, **kwargs):
        form = forms.AddItemToCartForm(request.POST)

        if form.is_valid():
            product_id = self.kwargs.get('product_id')
            cart, _ = models.Cart.objects.get_or_create(user=self.request.user)
            quantity = form.cleaned_data['quantity']
            cart_item, created = models.CartItem.objects.get_or_create(product_id=product_id, cart=cart)

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save(update_fields=['quantity'])

        logger.info("Yay! Item added to cart")

        return redirect(reverse('cart:cart'))


class RemoveCartItemView(generic.DeleteView):
    model = models.CartItem
    success_url = reverse_lazy('cart:cart')

    def get_queryset(self):
        # not strictly needed for functionality but good to do for security purposes
        return models.CartItem.objects.filter(cart__user=self.request.user)


class DecrementCartItemQuantityView(generic.View):
    model = models.CartItem

    def post(self, request, *args, **kwargs):
        cart_item = models.CartItem.objects.get(pk=self.kwargs.get('pk'))

        if cart_item.quantity == 1:
            cart_item.quantity = 0
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save(update_fields=['quantity'])

        return redirect(reverse('cart:cart'))


class IncrementCartItemQuantityView(generic.View):
    modes = models.CartItem

    def post(self, request, *args, **kwargs):
        cart_item = models.CartItem.objects.get(pk=self.kwargs.get('pk'))

        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

        return redirect(reverse('cart:cart'))
