from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import ShippingDetails


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ShippingDetailsCreateForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        exclude = ['user', 'status', 'is_default']


class ShippingDetailsSelectForm(forms.Form):
    shipping_details = forms.ModelChoiceField(
        queryset=ShippingDetails.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['shipping_details'].queryset = ShippingDetails.objects.filter(user=user)
