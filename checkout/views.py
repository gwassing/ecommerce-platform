from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsForm
from accounts.models import Order
from cart.models import Cart


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        cart_items = Cart.objects.get(user=self.request.user).cart_items.all()  # prefetch or select_related?

        return super().get_context_data(**kwargs) | {
            "cart_items": cart_items,
            "shipping_form": ShippingDetailsForm()
        }

    def post(self, request, *args, **kwargs):
        form = ShippingDetailsForm(data=request.POST)
        print(form.data)

        if form.is_valid():
            print('form is valid')
            shipping_details_obj = form.save(commit=False)
            shipping_details_obj.user = request.user
            shipping_details_obj.save()

            print('shipping details obj', shipping_details_obj)

            order = Order.objects.create(
                user=request.user,
                purchased_items=request.user.cart,
                shipping_details=shipping_details_obj
            )
            print('order obj', order)

            return redirect(reverse('checkout:order_confirmation'))

        # context is created so that form is displayed with fields pre-filled in case form is not valid
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
