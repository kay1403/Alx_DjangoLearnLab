from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200, label='Book Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
