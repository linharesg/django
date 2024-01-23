from django.db import models
from django.utils.text import slugify

class Products(models.Model):
    
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.DecimalField(max_digits=11, decimal_places=2)
    is_perishable = models.BooleanField()
    expiration_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to="uploads")
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"