from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from accounts.forms import ShippingDetailsSelectForm, ShippingDetailsCreateForm, PaymentDetailsCreateForm, \
    PaymentDetailsSelectForm
from accounts.models import Order, PurchasedItem, ShippingDetails, PaymentDetails


class CreateOrderMixin:
    def create_order_and_clear_cart(self):
        address_id = self.request.session.get('checkout_address_id')
        payment_id = self.request.session.get('checkout_payment_id')

        user = self.request.user
        # create an order with the user's shipping details
        order = Order.objects.create(
            user=user,
            shipping_details_id=address_id,
            payment_details_id=payment_id
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

        # send email
        message = render_to_string('emails/order_confirmation.txt', {
            'user': user,
            'order': order,
            'purchased_items': order.purchased_items.all(),
        })

        send_mail(
            "Order confirmed!",
            message,
            "info@gabylando.com",
            [user.email],
        )

        return reverse('checkout:order_confirmation')


class CheckoutShippingDetailsSelectView(LoginRequiredMixin, generic.FormView):
    template_name = 'checkout/checkout_address.html'
    form_class = ShippingDetailsSelectForm

    def get(self, request, *args, **kwargs):
        if not ShippingDetails.objects.filter(user=request.user).exists():
            return redirect('checkout:address_create')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        selected_address = form.cleaned_data['shipping_details']
        # Save to Django session
        self.request.session['checkout_address_id'] = selected_address.id
        print('selected_address:', selected_address)
        print('address id saved in session', self.request.session['checkout_address_id'])

        return redirect('checkout:payment')


class CheckoutShippingDetailsCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ShippingDetailsCreateForm
    template_name = 'checkout/checkout_address_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        self.request.session['checkout_address_id'] = self.object.id
        print('created_address:', self.object.id)
        print('address id saved in session:', self.request.session['checkout_address_id'])

        return redirect('checkout:payment')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'shipping_details': ShippingDetails.objects.filter(user=self.request.user)
        }


class CheckoutPaymentDetailsSelectView(LoginRequiredMixin, CreateOrderMixin, generic.FormView):
    form_class = PaymentDetailsSelectForm
    template_name = 'checkout/checkout_payment.html'

    def get(self, request, *args, **kwargs):
        if not PaymentDetails.objects.filter(user=request.user).exists():
            return redirect('checkout:payment_create')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        selected_payment_details = form.cleaned_data['payment_details']
        self.request.session['checkout_payment_id'] = selected_payment_details.id
        print('selected payment details', selected_payment_details)
        print('payment id saved in session', self.request.session['checkout_payment_id'])

        return redirect(self.create_order_and_clear_cart())


class CheckoutPaymentDetailsCreateView(LoginRequiredMixin, CreateOrderMixin, generic.CreateView):
    template_name = 'checkout/checkout_payment_create.html'
    form_class = PaymentDetailsCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        self.request.session['checkout_payment_id'] = self.object.id
        print('created_payment_details:', self.object.id)
        print('payment id saved in session', self.request.session['checkout_payment_id'])

        return redirect(self.create_order_and_clear_cart())

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "payment_details": PaymentDetails.objects.filter(user=self.request.user)
        }


class OrderConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/order_confirmation.html'

    def get_context_data(self, **kwargs):
        latest_order = Order.objects.filter(user=self.request.user).last()
        purchased_items = PurchasedItem.objects.filter(order=latest_order).select_related('product')

        return super().get_context_data(**kwargs) | {
            'purchased_items': purchased_items
        }
