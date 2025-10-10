from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsSelectForm
from accounts.models import Order, PurchasedItem, ShippingDetails


class CreateOrderMixin:
    def create_order_and_clear_cart(self, shipping_details):
        user = self.request.user
        # create an order with the user's shipping details
        order = Order.objects.create(
            user=user,
            shipping_details=shipping_details
        )

        # transform user's cart items into purchased items and add to order object
        for item in user.cart.cart_items.all():
            PurchasedItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # empty cart
        user.cart.cart_items.all().delete()
        return reverse('checkout:order_confirmation')


class CheckoutShippingDetailsSelectView(LoginRequiredMixin, generic.FormView):
    template_name = 'checkout/checkout_address.html'
    form_class = ShippingDetailsSelectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        selected_address = form.cleaned_data['shipping_details']
        # Save to Django session
        self.request.session['checkout_address_id'] = selected_address.id
        print(f"✅ Stored address ID {selected_address.id} in session")

        return redirect('checkout:payment')


class CheckoutPaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout_payment.html'


class ExistingShippingDetailsRedirectView(LoginRequiredMixin, CreateOrderMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        shipping_details_obj = ShippingDetails.objects.get(
            pk=kwargs['pk'],
            user=self.request.user
        )

        return self.create_order_and_clear_cart(shipping_details_obj)


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
