from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views


app_name = 'listings'

urlpatterns = [
  path('', views.product_list, name='product_list'),

  path(_('favorite/'), views.product_fav, name='favorite'),
  
  path('<slug:category_slug>/', views.product_list, 
    name='product_list_by_category'),
  
  path('<slug:category_slug>/<slug:product_slug>/',
    views.product_detail, name='product_detail'),
]
