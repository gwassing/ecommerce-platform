from django import forms
from . import models


class CreateCartItemForm(forms.ModelForm):
    class Meta:
        model = models.CartItem
        fields = []  # empty for now, use quantity field later
