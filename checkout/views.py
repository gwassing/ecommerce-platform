from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsForm
from accounts.models import Order, PurchasedItem, ShippingDetails


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        cart = self.request.user.cart
        default_shipping_address = ShippingDetails.objects.filter(
            user=self.request.user,
            is_default=True
        )

        last_used_shipping_address = ShippingDetails.objects.filter(user=self.request.user)

        return super().get_context_data(**kwargs) | {
            "cart_items": cart.get_items(),
            "total_price": cart.get_total_price(),
            "shipping_form": ShippingDetailsForm(),
            "default_shipping_address": default_shipping_address.first() if default_shipping_address.exists() else None,
            "last_used_shipping_address": last_used_shipping_address.last() if last_used_shipping_address.exists() else None,
        }

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'create_new_shipping_address':
            form = ShippingDetailsForm(data=request.POST)

            if form.is_valid():
                # attach user to shipping details form instance
                shipping_details_obj = form.save(commit=False)
                shipping_details_obj.user = request.user
                shipping_details_obj.save()
            else:
                # If the form is invalid, get the standard context and then add the invalid form object to it.
                context = self.get_context_data()
                context['shipping_form'] = form
                return render(request, self.template_name, context)

        elif action == 'use_default_shipping_address':
            default_shipping_address = ShippingDetails.objects.filter(
                user=self.request.user,
                is_default=True
            ).first()
            shipping_details_obj = default_shipping_address

        elif action == 'use_last_used_shipping_address':
            last_used_shipping_address = ShippingDetails.objects.filter(user=self.request.user).last()
            shipping_details_obj = last_used_shipping_address

        # create an order with the user's shipping details
        order = Order.objects.create(
            user=request.user,
            shipping_details=shipping_details_obj
        )

        # transform user's cart items into purchased items and add to order object
        for item in request.user.cart.cart_items.all():
            PurchasedItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # empty cart
        request.user.cart.cart_items.all().delete()

        return redirect(reverse('checkout:order_confirmation'))


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
