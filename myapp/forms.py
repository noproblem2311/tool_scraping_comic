# myapp/forms.py
from django import forms

class FilterForm(forms.Form):
    min_rating = forms.FloatField(label='Rating tối thiểu', required=True)
    link = forms.URLField(label='Link truyện', required=True)
