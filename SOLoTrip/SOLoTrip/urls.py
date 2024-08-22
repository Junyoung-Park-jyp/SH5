from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bank_accounts/', include('bank_accounts.urls')),
    path('exchange_rates/', include('exchange_rates.urls')),
    path('trips/', include('trips.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
