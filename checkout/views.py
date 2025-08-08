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

        try:
            default_shipping_details = ShippingDetails.objects.get(
                user=self.request.user,
                is_default=True
            )
        except ShippingDetails.DoesNotExist:
            default_shipping_details = None

        last_used_shipping_details = Order.objects.latest('pk').shipping_details

        return super().get_context_data(**kwargs) | {
            "cart_items": cart.get_items(),
            "total_price": cart.get_total_price(),
            "shipping_form": ShippingDetailsForm(),
            "existing_shipping_details": default_shipping_details if default_shipping_details else last_used_shipping_details,
        }

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'create_new_shipping_details':
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
        elif action == 'use_existing_shipping_details':
            existing_shipping_details = ShippingDetails.objects.filter(
                user=self.request.user,
                is_default=True
            ).first() or ShippingDetails.objects.filter(user=self.request.user).last()
            shipping_details_obj = existing_shipping_details

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
