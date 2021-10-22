from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
#from orders.views import apple_pay


urlpatterns = i18n_patterns(
    #path('.well-known/apple-developer-merchantid-domain-association/', apple_pay),
    path(_('accounts/'), include('accounts.urls')),
    path('social-auth/', 
        include('social_django.urls', namespace='social')),
    path(_('admin/'), admin.site.urls),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path('rosetta/', include('rosetta.urls')),
    path('', include('listings.urls', namespace='listings'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)
