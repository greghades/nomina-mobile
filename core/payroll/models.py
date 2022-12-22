from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Payroll(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL) 
    payment_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"{self.user} - {self.payment_date}"