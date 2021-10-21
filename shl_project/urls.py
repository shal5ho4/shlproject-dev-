from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from orders.views import apple_pay


urlpatterns = [
    #path('.well-known/apple-developer-merchantid-domain-association/', apple_pay),
    path('accounts/', include('accounts.urls')),
    path('social-auth/', 
        include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('listings.urls', namespace='listings'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)
