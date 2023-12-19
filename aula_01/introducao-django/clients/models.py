from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField()
    cpf = models.CharField(max_length = 20)
    zipcode = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 20)
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 2)
    enabled = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.name