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


class CheckoutAddressView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout_address.html'

    def get_context_data(self, **kwargs):
        try:
            existing_shipping_details = ShippingDetails.objects.filter(user=self.request.user).distinct()
        except ShippingDetails.DoesNotExist:
            existing_shipping_details = None

        return super().get_context_data(**kwargs) | {
            "shipping_form": ShippingDetailsForm(),
            "existing_shipping_details": existing_shipping_details,

        }

    def post(self, request, *args, **kwargs):
        selected_address_id = request.POST.get('shipping_address')

        if selected_address_id:
            # Verify address belongs to user
            try:
                ShippingDetails.objects.get(
                    pk=selected_address_id,
                    user=request.user
                )
                # Save to Django session
                request.session['checkout_address_id'] = selected_address_id
                print(f"✅ Stored address ID {selected_address_id} in session")

                return redirect('checkout:payment')

            except ShippingDetails.DoesNotExist:
                print("Invalid address selection")
                return redirect('checkout:address')
        else:
            # No address selected
            print("Please select an address")
            return redirect('checkout:address')


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
