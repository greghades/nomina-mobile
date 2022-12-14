from django.db import models
from authentication.models import CustomUser

class Nomina(models.Model):
    id_nomina = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=False)
    date = models.DateField(null=False)
