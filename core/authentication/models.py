from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Roles(models.Model):
    rol_name = models.CharField(max_length=50)

    def __str__(self):
        return self.rol_name

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    code_employee = models.CharField(max_length=15,null=False,unique=True)
    ine = models.CharField(max_length=20, null=False)
    rfc = models.CharField(max_length=15, null=False)
    nss = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=150,null=False)
    status = models.BooleanField(default=False)
    date_start = models.DateField(blank=True,null=True)
    rol = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, null=True, blank=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.get_full_name()}"