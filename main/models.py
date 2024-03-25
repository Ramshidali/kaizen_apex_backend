import uuid
from django.db import models

from versatileimagefield.fields import VersatileImageField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, null=True,
                                related_name="updater_%(class)s_objects", on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        
        
class Branches(BaseModel):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    image = VersatileImageField('Image', upload_to="main/branches")
    
    class Meta:
        db_table = 'web_branches'
        verbose_name = ('Web Branches')
        verbose_name_plural = ('Web Branches')
    
    def __str__(self):
        return str(self.id)