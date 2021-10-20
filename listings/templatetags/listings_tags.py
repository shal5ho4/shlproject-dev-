from django import template
from ..forms import SearchForm


register = template.Library()

@register.inclusion_tag('product/search_bar.html')
def search_bar():
    form = SearchForm()
    return {'form': form}