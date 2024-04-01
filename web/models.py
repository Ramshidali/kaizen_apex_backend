import uuid
from django.db import models

from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField

from main.models import BaseModel, Branches
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
    logo = VersatileImageField('Logo', upload_to="web/our_features",null=True,blank=True)
    
    class Meta:
        db_table = 'web_our_features'
        verbose_name = ('Web Features')
        verbose_name_plural = ('Web Features')
    
    def __str__(self):
        return str(self.id)
    
class CustomerReviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    name = models.CharField(max_length=200)
    ocupation = models.CharField(max_length=200)
    email = models.EmailField()
    review = models.TextField()
    image = VersatileImageField('Image', upload_to="web/customer_review")
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'web_customer_review'
        verbose_name = ('Web Customer Review')
        verbose_name_plural = ('Web Customer Review')
    
    def __str__(self):
        return str(self.id)
    
class Blog(BaseModel):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    ocupation = models.CharField(max_length=200)
    email = models.EmailField()
    review = RichTextUploadingField()
    image = VersatileImageField('Image', upload_to="web/customer_review")
    
    class Meta:
        db_table = 'web_blog'
        verbose_name = ('Web Blog')
        verbose_name_plural = ('Web Blog')
    
    def __str__(self):
        return str(self.id)
    
class Contact(BaseModel):
    address = models.TextField()
    location = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    facebook = models.URLField()
    instagram = models.URLField()
    youtube = models.URLField()
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE,null=True)
    main = models.BooleanField(default=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'web_contact'
        verbose_name = ('Web Contact')
        verbose_name_plural = ('Web Contact')
    
    def __str__(self):
        return str(self.id)
    
class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    complaint = models.TextField()
    email = models.EmailField()
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'web_complaint'
        verbose_name = ('Web Complaint')
        verbose_name_plural = ('Web Complaint')
    
    def __str__(self):
        return str(self.id)
    
class Enquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=20)
    description = models.TextField()
    email = models.EmailField()
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'web_enquiry'
        verbose_name = ('Web Enquiry')
        verbose_name_plural = ('Web Enquiry')
    
    def __str__(self):
        return str(self.id)