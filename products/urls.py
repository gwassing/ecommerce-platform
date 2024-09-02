from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="index"),
    path("<int:pk>", views.ProductDetailView.as_view(), name="product_detail")
]
