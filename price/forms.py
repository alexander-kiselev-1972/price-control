from django import forms


class LekSearch(forms.Form):
    barcode = forms.CharField(max_length=13)


