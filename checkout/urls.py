from django.urls import path

from checkout import views

app_name = 'checkout'

urlpatterns = [
    path("address/", views.CheckoutShippingDetailsSelectView.as_view(), name="address"),
    path("payment/", views.CheckoutPaymentView.as_view(), name="payment"),
    path('confirmation/', views.OrderConfirmationView.as_view(), name="order_confirmation")
]
