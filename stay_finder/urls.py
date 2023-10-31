from django.contrib import admin
from django.urls import path,include
from vendor import urls as vendor_urls
from django.conf import settings
from django.conf.urls.static import static
from tier import urls as tier_urls
from payment import urls as payment_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendor/',include(vendor_urls)),
    path('tier/',include(tier_urls)),
    path('payment/',include(payment_urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
