from django.urls import path

from checkout import views

app_name = 'checkout'

urlpatterns = [
    path('', views.CheckoutView.as_view(), name="checkout"),
    path('<int:pk>/', views.ExistingShippingDetailsRedirectView.as_view(), name="existing_shipping_details_redirect"),
    path('confirmation/', views.OrderConfirmationView.as_view(), name="order_confirmation")
]
