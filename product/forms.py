from django.forms.widgets import TextInput,FileInput,Textarea,Select
from django import forms

from . models import *
        
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}), 
        }
        
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name','category','image','have_varient']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}), 
            'category': Select(attrs={'class': 'required form-control'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
class ProductVarientForm(forms.ModelForm):

    class Meta:
        model = ProductVarient
        fields = ['name','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }