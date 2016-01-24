import evbrite
from django import forms

class CategoryForm(forms.Form):
    input_choices = evbrite.categories_to_id_pairs(evbrite.get_categories().get('categories'))
    location = forms.CharField(label='Location', max_length=100)
    category_ids = forms.MultipleChoiceField(choices=input_choices, widget=forms.CheckboxSelectMultiple())
