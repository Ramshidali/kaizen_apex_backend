import uuid
from django.db import models
from versatileimagefield.fields import VersatileImageField
from main.models import BaseModel

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'product_category'
        verbose_name = ('Product Category')
        verbose_name_plural = ('Product Category')
    
    def __str__(self):
        return str(self.name)
    
    def get_products(self):
        product = Product.objects.filter(category=self)
        return product
    
class Product(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    image = VersatileImageField('Image', upload_to="product/product_image", blank=True, null=True)
    have_varient = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'product_product'
        verbose_name = ('Product')
        verbose_name_plural = ('Product')
    
    def __str__(self):
        return str(self.name)
    
    def get_varients(self):
        varient = ProductVarient.objects.filter(product=self,is_deleted=False).order_by("-product__date_added")
        return varient
    
class ProductVarient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = VersatileImageField('Image', upload_to="product/product_varient_image", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'product_product_varient'
        verbose_name = ('Product Varient')
        verbose_name_plural = ('Product Varient')
    
    def __str__(self):
        return str(self.name)