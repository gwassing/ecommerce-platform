from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout/checkout.html'
