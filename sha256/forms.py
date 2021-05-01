from django import forms
from .models import Hash


class HashForm(forms.ModelForm):

    class Meta:
        model = Hash
        fields = 'text',
        widgets = {
            'text': forms.Textarea
        }

    def save(self, commit=True, user=None, hash=None):
        text = self.cleaned_data.get('text')
        instance = Hash(user=user, text=text, hash=hash)
        instance.save()
        return instance
