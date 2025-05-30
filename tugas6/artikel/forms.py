from django import forms 
from artikel.models import Kategori, Artikel

class KategoriForms(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama',]
        widgets = {
            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
        }