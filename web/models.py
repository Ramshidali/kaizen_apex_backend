import uuid
from django.db import models

from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField

from main.models import BaseModel
from product.models import Product

# Create your models here.
class Banner(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    image = VersatileImageField('Image', upload_to="web/banner_image")
    
    class Meta:
        db_table = 'web_banner'
        verbose_name = ('Web Banner')
        verbose_name_plural = ('Web Banner')
    
    def __str__(self):
        return str(self.id)
    
class AboutUs(BaseModel):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    image = VersatileImageField('Image', upload_to="web/about_us")
    
    class Meta:
        db_table = 'web_about_us'
        verbose_name = ('Web About Us')
        verbose_name_plural = ('Web About Us')
    
    def __str__(self):
        return str(self.id)
    
class OurFeatures(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    logo = VersatileImageField('Logo', upload_to="web/our_features")
    
    class Meta:
        db_table = 'web_our_features'
        verbose_name = ('Web Features')
        verbose_name_plural = ('Web Features')
    
    def __str__(self):
        return str(self.id)
    
class CustomerReviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    ocupation = models.CharField(max_length=200)
    email = models.EmailField()
    review = models.TextField()
    image = VersatileImageField('Image', upload_to="web/customer_review")
    
    class Meta:
        db_table = 'web_customer_review'
        verbose_name = ('Web Customer Review')
        verbose_name_plural = ('Web Customer Review')
    
    def __str__(self):
        return str(self.id)
    
class Blog(BaseModel):
    name = models.CharField(max_length=200)
    ocupation = models.CharField(max_length=200)
    email = models.EmailField()
    review = models.TextField()
    image = VersatileImageField('Image', upload_to="web/customer_review")
    
    class Meta:
        db_table = 'web_blog'
        verbose_name = ('Web Blog')
        verbose_name_plural = ('Web Blog')
    
    def __str__(self):
        return str(self.id)
    
class Contact(BaseModel):
    address = models.TextField()
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    facebook = models.URLField()
    instagram = models.URLField()
    youtube = models.URLField()
    linkedin = models.URLField()
    
    class Meta:
        db_table = 'web_contact'
        verbose_name = ('Web Contact')
        verbose_name_plural = ('Web Contact')
    
    def __str__(self):
        return str(self.id)
    
class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    
    class Meta:
        db_table = 'web_complaint'
        verbose_name = ('Web Complaint')
        verbose_name_plural = ('Web Complaint')
    
    def __str__(self):
        return str(self.id)