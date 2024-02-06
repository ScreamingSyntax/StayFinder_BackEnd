from django.contrib import admin
from django.urls import path,include
from vendor import urls as vendor_urls
from django.conf import settings
from django.conf.urls.static import static
from tier import urls as tier_urls
from customer import urls as customer_urls
from accomodation import urls as accomodation_urls
from booking import urls as booking_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendor/',include(vendor_urls)),
    path('tier/',include(tier_urls),
         ),
    path("accommodation/", include(accomodation_urls), name=""),
    path("customer/",include(customer_urls)),
    path("book/",include(booking_urls))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
