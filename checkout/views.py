from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsForm
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


class CheckoutView(LoginRequiredMixin, CreateOrderMixin, generic.TemplateView):
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        cart = self.request.user.cart

        try:
            default_shipping_details = ShippingDetails.objects.get(
                user=self.request.user,
                is_default=True
            )
        except ShippingDetails.DoesNotExist:
            default_shipping_details = None

        try:
            last_used_shipping_details = Order.objects.filter(user=self.request.user).latest('pk').shipping_details
        except Order.DoesNotExist:
            last_used_shipping_details = None

        return super().get_context_data(**kwargs) | {
            "cart_items": cart.get_items(),
            "total_price": cart.get_total_price(),
            "shipping_form": ShippingDetailsForm(),
            "existing_shipping_details": default_shipping_details if default_shipping_details else last_used_shipping_details,
        }

    def post(self, request, *args, **kwargs):
        form = ShippingDetailsForm(data=request.POST)

        if form.is_valid():
            # attach user to shipping details form instance
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()
            return self.create_order_and_clear_cart(shipping_details)
        else:
            # If the form is invalid, get the standard context and then add the invalid form object to it.
            context = self.get_context_data()
            context['shipping_form'] = form
            return render(request, self.template_name, context)


class ExistingShippingDetailsRedirectView(LoginRequiredMixin, CreateOrderMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        shipping_details_obj = ShippingDetails.objects.get(
            pk=kwargs['pk'],
            user=self.request.user
        )

        return self.create_order_and_clear_cart(shipping_details_obj)


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
