from django import forms


class HashForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
