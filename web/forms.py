from django.forms.widgets import TextInput,FileInput,Textarea,Select
from django import forms

from . models import *
        
class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['product','image']

        widgets = {
            'product': Select(attrs={'class': 'required form-control'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
        
class OurFeaturesForm(forms.ModelForm):

    class Meta:
        model = OurFeatures
        fields = ['title','description','logo']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Title"}),
            'description': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Description"}),
            'logo': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
class AboutUsForm(forms.ModelForm):

    class Meta:
        model = AboutUs
        fields = ['title','description','image']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Title"}),
            'description': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Description"}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
class CustomerReviewsForm(forms.ModelForm):

    class Meta:
        model = CustomerReviews
        fields = ['name','ocupation','email','review','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Name"}),
            'ocupation': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Ocupation"}),
            'email': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Email"}),
            'review': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Review"}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['name','title','ocupation','email','review','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Your Name"}),
            'ocupation': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Ocupation"}),
            'email': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Email"}),
            'title': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Title"}),
            # 'review': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Review"}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['address','latitude','location','longitude','phone','email','facebook','instagram','youtube','branch','main']

        widgets = {
            'address': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Address"}),
            'location': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Location"}),
            'latitude': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Latitude"}),
            'longitude': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Longitude"}),
            'phone': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Phone"}),
            'email': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Email"}),
            'facebook': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Facebook"}),
            'instagram': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Instagram"}),
            'youtube': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Youtube"}),
            'branch': Select(attrs={'class': 'required form-control'}),
        }
        
class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['name','complaint','email']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control bg-transparent w-100 my-2','placeholder':"Enter Name"}),
            'complaint': Textarea(attrs={'class': 'form-control bg-transparent w-100 my-2','rows':'2','placeholder':"Enter Complaint"}),
            'email': TextInput(attrs={'class': 'form-control bg-transparent w-100 my-2','placeholder':"Enter Email"}),
        }
        
class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry
        fields = ['name','description','subject','email']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Name"}),
            'subject': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Subject"}),
            'description': Textarea(attrs={'class': 'required form-control','placeholder':"Enter Description","style":"height:220px;"}),
            'email': TextInput(attrs={'class': 'required form-control','placeholder':"Enter Email"}),
        }
        
