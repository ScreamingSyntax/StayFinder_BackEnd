from django.contrib import admin
from django.urls import path,include
from vendor import urls as vendor_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendor/',include(vendor_urls))

]
