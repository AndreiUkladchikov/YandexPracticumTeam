from django import forms


class CheckPromocodeForms(forms.Form):
    user_id = forms.UUIDField()
    promocode = forms.CharField()
