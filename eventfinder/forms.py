import evbrite
from django import forms

class CategoryForm(forms.Form):
    # User's location
    location = forms.CharField(label='Location', max_length=100)
    # Categories from eventbrite API
    input_choices = evbrite.categories_to_id_pairs(evbrite.get_categories().get('categories'))
    category_ids = forms.MultipleChoiceField(choices=input_choices, widget=forms.CheckboxSelectMultiple(attrs={'class': 'display_categories'}))
