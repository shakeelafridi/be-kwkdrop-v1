from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authModule.urls')),
    path('api/seller/', include('seller.urls')),
    path('api/buyer/',include('buyer.urls')),
    path('api/driver/',include('driver.urls')),
    path('api/payments/', include('payments.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
