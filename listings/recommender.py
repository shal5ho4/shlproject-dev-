from django.conf import settings
from .models import Product
import redis

# Establish a connection
r = redis.Redis(host=settings.REDIS_HOST, 
  port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):

  # Build a redis key
  def get_product_key(self, id):
    
    return f'product:{id}:purchased_with'
  

  # Recieve a list of products
  # that have been bought together 
  def products_bought(self, products):
    
    product_ids = [p.id for p in products]
    
    for product_id in product_ids:
      for with_id in product_ids:
        
        if product_id != with_id:
          r.zincrby(self.get_product_key(product_id), 1, with_id)


  def suggest_products_for(self, products, max_results=3):

    product_ids = [p.id for p in products]

    # Only one product
    if len(products) == 1:
      suggestions = r.zrange(
        self.get_product_key(product_ids[0]), 0, -1, desc=True
      )[:max_results]
    
    else:
      # Generate a tmp key
      flat_ids = ''.join(str(id) for id in product_ids)
      tmp_key = f'tmp_{flat_ids}'

      # Combine scores of all products
      # Store the resulting sorted set in a tmp key
      keys = [self.get_product_key(id) for id in product_ids]
      r.zunionstore(tmp_key, keys)

      # Remove ids for the products the recommendation is for
      r.zrem(tmp_key, *product_ids)

      # Get the product ids by their score in decendant order
      suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

      # Remove the tmp key
      r.delete(tmp_key)
    
    suggested_products_ids = [int(id) for id in suggestions]

    # Get suggested products and sort by order of appearance
    suggested_products = list(
      Product.objects.filter(id__in=suggested_products_ids)
    )
    suggested_products.sort(
      key=lambda x: suggested_products_ids.index(x.id)
    )
    return suggested_products


  def clear_purchases(self):

    for id in Product.objects.values_list('id', flat=True):
      r.delete(self.get_product_key(id))
