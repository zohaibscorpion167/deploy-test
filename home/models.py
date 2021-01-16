from django.db import models
from io import BytesIO
from django.core.files import File

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=124, null=False, blank=False)
    email = models.CharField(max_length=124, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class ImageUpload(models.Model):
    pic = models.ImageField(upload_to='texttoimage')

        
        

    