from django.forms.widgets import TextInput,FileInput,Textarea,Select
from django import forms

from . models import *
        
                
class BranchesForm(forms.ModelForm):

    class Meta:
        model = Branches
        fields = ['name','location','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Name"}),
            'location': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Location"}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }