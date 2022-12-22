from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

# Create your models here.
class Roles(models.Model):
    rol_name = models.CharField(max_length=50)

    def __str__(self):
        return self.rol_name

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    code_employee = models.CharField(max_length=15,null=True)
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



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_link = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        
        "Password Reset Link for {title}".format(title="Syncronik Payroll App"),
        
        # message:
        reset_link,
        # from:
        "noreply@syncronik.com",
        # to:
        [reset_password_token.user.email]
    )