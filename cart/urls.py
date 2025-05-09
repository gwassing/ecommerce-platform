from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart'),
    path('add/<int:product_id>', views.AddItemToCartView.as_view(), name="add_to_cart"),
    path('remove/<int:pk>', views.RemoveCartItemView.as_view(), name="remove_from_cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
]
