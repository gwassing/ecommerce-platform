from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.IndexView.as_view(), name="index"),
    path('products/', include("products.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('cart/', include("cart.urls")),
    path('checkout/', include("checkout.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
