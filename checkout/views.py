from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsForm
from accounts.models import Order, PurchasedItem
from cart.models import Cart


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "cart_items": Cart.objects.get(user=self.request.user).get_cart_items(),
            "total_price": Cart.objects.get(user=self.request.user).get_total_cart_price(),
            "shipping_form": ShippingDetailsForm()
        }

    def post(self, request, *args, **kwargs):
        form = ShippingDetailsForm(data=request.POST)

        if form.is_valid():
            # attach user to shipping details form instance
            shipping_details_obj = form.save(commit=False)
            shipping_details_obj.user = request.user
            shipping_details_obj.save()

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

        # context is created so that form is displayed with fields pre-filled in case form is not valid
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
