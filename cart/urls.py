from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart'),
    path('add/<int:product_id>', views.AddItemToCartView.as_view(), name="add_to_cart"),
    path('remove/<int:pk>', views.RemoveCartItemView.as_view(), name="remove_from_cart"),
    path('decrement/<int:pk>', views.DecrementCartItemQuantityView.as_view(), name="decrement_quantity"),
    path('increment/<int:pk>', views.IncrementCartItemQuantityView.as_view(), name="increment_quantity"),
]
