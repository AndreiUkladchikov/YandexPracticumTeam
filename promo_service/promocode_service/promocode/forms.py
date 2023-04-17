from django import forms


class CheckPromocodeForms(forms.Form):
    """Form to check user promocode."""
    user_id = forms.UUIDField()
    promocode = forms.CharField()
