from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsSelectForm, ShippingDetailsCreateForm
from accounts.models import Order, PurchasedItem


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
        print('selected_address:', selected_address)

        return redirect(self.place_order_and_clear_cart())

    def place_order_and_clear_cart(self):
        selected_address_id = self.request.session.get('checkout_address_id')

        user = self.request.user
        # create an order with the user's shipping details
        order = Order.objects.create(
            user=user,
            shipping_details_id=selected_address_id
        )

        # transform user's cart items into purchased items and add to order object
        for item in user.cart.cart_items.all():
            PurchasedItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        print('purchased items:', order.purchased_items.all())

        # empty cart
        user.cart.cart_items.all().delete()
        return reverse('checkout:order_confirmation')


class CheckoutShippingDetailsCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ShippingDetailsCreateForm
    template_name = 'checkout/checkout_address_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        self.request.session['checkout_address_id'] = self.object.id
        print('created_address:', self.object.id)

        return redirect(self.place_order_and_clear_cart())

    def place_order_and_clear_cart(self):
        created_address_id = self.request.session.get('checkout_address_id')

        user = self.request.user
        # create an order with the user's shipping details
        order = Order.objects.create(
            user=user,
            shipping_details_id=created_address_id
        )

        # transform user's cart items into purchased items and add to order object
        for item in user.cart.cart_items.all():
            PurchasedItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        print('purchased items:', order.purchased_items.all())

        # empty cart
        user.cart.cart_items.all().delete()
        return reverse('checkout:order_confirmation')


class CheckoutPaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout_payment.html'


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'
