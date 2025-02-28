from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart'),
    path('add/<int:product_id>', views.CreateCartItemView.as_view(), name="add_to_cart"),
]
