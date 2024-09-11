from django.db import models

# Create your models here.
from django.db import models

class ImageCaption(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.TextField()

    def __str__(self):
        return self.caption
