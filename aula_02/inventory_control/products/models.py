from django.db import models
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from suppliers.models import Supplier

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    
    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
class Products(models.Model):
    
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.DecimalField(max_digits=11, decimal_places=2)
    is_perishable = models.BooleanField()
    expiration_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to="products")
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    # suppliers = models.ManyToManyField(Supplier)
    suppliers = models.ManyToManyField(
        Supplier,
        through="SupplierProduct",
        through_fields=("product", "supplier"),
        blank=True
    )
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.__update_is_perishable()

        # Removendo a imagem antiga
        if self.pk: # Vai validar se está alterando ou criando novo
            old_obj = Products.objects.filter(pk=self.pk).first()
            if old_obj and old_obj.photo != self.photo:
                self.__delete_file_if_exists(old_obj.photo)
            if old_obj and old_obj.thumbnail:
                self.__delete_file_if_exists(old_obj.thumbnail)

        super(Products, self).save(*args, **kwargs)

        # Criando a thumbnail
        self.__create_thumbnail()
        super(Products, self).save(*args, **kwargs)
        
    def __update_is_perishable(self):
        self.is_perishable = bool(self.expiration_date)

    def __create_thumbnail(self):
        if not self.photo:
            return

        img = Image.open(self.photo.path)  # Abrindo a imagem com o pillow
        size = (30, 30)  # Definindo o tamanho do redimensionamento
        img.thumbnail(size)  # Redimensionando a imagem

        # Salvando a imagem
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        # Definindo o nome do arquivo
        name, extension = os.path.splitext(
            self.photo.name)  # [nome-arquivo, .jpeg]
        thumb_filename = f"{name}_thumb{extension}"

        # Salvar a imagem na instância do produto
        self.thumbnail.save(thumb_filename, ContentFile(
            thumb_io.getvalue()), save=False)

    def __delete_file_if_exists(self, file):
        if file and os.path.isfile(file.path):
            os.remove(file.path)

    def delete(self, *args, **kwargs):
        self.__delete_file_if_exists(self.photo)
        super(Products, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        
class SupplierProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Fornecedor do produto"
        verbose_name_plural = "Fornecedores dos Produtos"
        unique_together = [["supplier", "product", "id"]]