from django.urls import path

from checkout import views

app_name = 'checkout'

urlpatterns = [
    path('', views.CheckoutView.as_view(), name="checkout"),
    path('<int:pk>/', views.CheckoutExistingShippingDetailsView.as_view(), name="checkout_existing_shipping_details"),
    path('confirmation/', views.OrderConfirmationView.as_view(), name="order_confirmation")
]
