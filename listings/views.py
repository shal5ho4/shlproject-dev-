from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
  SearchVector, SearchQuery, SearchRank
)
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .models import Category, Product, Review
from .forms import ReviewForm, SearchForm


def product_list(request, category_slug=None):

  language = request.LANGUAGE_CODE

  categories = Category.objects.all()
  requested_category = None
  products = Product.objects.all()

  form = SearchForm()
  query = None

  paginator = Paginator(products, 9)
  page = request.GET.get('page')

  try:
    products = paginator.page(page)
  except PageNotAnInteger:
    products = paginator.page(1)
  except EmptyPage:
    products = paginator.page(paginator.num_pages)

  if 'query' in request.GET:
    form = SearchForm(request.GET)

    if form.is_valid():
      query = form.cleaned_data['query']
      search_vector = SearchVector('name', weight='A') + \
                      SearchVector('description', weight='B')
      search_query = SearchQuery(query)

      # performing stemming search
      # weighting queries
      products = Product.objects.annotate(
        search=search_vector, rank=SearchRank(
          search_vector, search_query
        )).filter(rank__gte=0.3).order_by('-rank')

  if category_slug:
    requested_category = get_object_or_404(Category,
      translations__language_code=language, 
      translations__slug=category_slug)
    products = Product.objects.filter(category=requested_category)

  return render(request, 'product/list.html', {
    'categories': categories, 'products': products,
    'requested_category': requested_category, 'page': page, 
    'query': query
  })


def product_detail(request, category_slug, product_slug):

  language = request.LANGUAGE_CODE

  category = get_object_or_404(Category, 
    translations__language_code=language,
    translations__slug=category_slug)
  product = get_object_or_404(Product, 
    category_id=category.id, slug=product_slug)
  
  r = Recommender()
  recommendation = r.suggest_products_for([product], 3)
  
  if request.method == 'POST':
    review_form = ReviewForm(request.POST)

    if review_form.is_valid():
      cf = review_form.cleaned_data
      author_name = 'Anonymous'

      if request.user.is_authenticated and request.user.first_name != '':
        author_name = request.user.first_name
      
      Review.objects.create(
        product=product, author=author_name, 
        rating=cf['rating'], text=cf['text']
      )
      return redirect('listings:product_detail',
        category_slug=category_slug, product_slug=product_slug)
  
  else:
    review_form = ReviewForm()
    cart_product_form = CartAddProductForm()
  
  return render(request, 'product/detail.html', {
    'product': product, 'review_form': review_form, 
    'cart_product_form': cart_product_form,
    'recommendation': recommendation
  })
  

@login_required
@require_POST
def product_fav(request):
  
  product_id = request.POST.get('id')
  action = request.POST.get('action')

  if product_id and action:
    try:
      product = Product.objects.get(id=product_id)
      if action == 'like':
        product.users_fav.add(request.user)
      else:
        product.users_fav.remove(request.user)
      
      return JsonResponse({'status':'ok'})
    
    except:
      pass
  
  return JsonResponse({'status':'error'})
