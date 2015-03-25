from django import forms

class Name(forms.Form):
    Name = forms.CharField(max_length=20)

