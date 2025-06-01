from django.urls import path

from checkout import views

app_name = 'checkout'

urlpatterns = [
    path('', views.CheckoutView.as_view(), name="checkout"),
    path('confirmation/', views.OrderConfirmationView.as_view(), name="order_confirmation")
]
