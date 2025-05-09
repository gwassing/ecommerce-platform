from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    path("brands/", views.BrandsListView.as_view(), name="brands_list"),
]
