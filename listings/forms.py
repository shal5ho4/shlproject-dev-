from django import forms
from django.forms.widgets import TextInput
from .models import Review


REVIEW_CHOICES = [
  ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
]


class ReviewForm(forms.ModelForm):

  class Meta:
    model = Review
    fields = ['text', 'rating']

    widgets = {
      'text': forms.Textarea(attrs={
        'class': 'form-control shadow px-2',
        'rows': 6
      }),
      'rating': forms.RadioSelect
    }


class SearchForm(forms.Form):

  query = forms.CharField(
    widget=TextInput(attrs={
      'class': 'form-control'
    })
  )
