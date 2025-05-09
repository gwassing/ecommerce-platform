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
        cart_items = self.object.cart_items.all().select_related('product')
        total_price = sum((item.product.price * item.quantity) for item in cart_items)
        total_items = cart_items.count()

        return super().get_context_data(**kwargs) | {
            "cart_items": cart_items,
            "total_items": total_items,
            "total_price": total_price,
            "cart_is_empty": total_items == 0
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


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cart/checkout.html'
