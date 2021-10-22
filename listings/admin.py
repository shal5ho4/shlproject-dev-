from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product, Review


class OrderReviewInline(admin.TabularInline):
  model = Review


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):

  list_display = ('name', 'slug')

  def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

  list_display = ('name', 'category', 'price', 'available')
  list_filter = ('category', 'available')
  list_editable = ('price', 'available')
  prepopulated_fields = {'slug': ('name',)}
  inlines = [OrderReviewInline]


admin.site.index_template = 'memcache_status/admin_index.html'