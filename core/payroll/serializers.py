from rest_framework import serializers
from .models import Payroll

class PayrollSerializer(serializers.ModelSerializer):
    code_employee = serializers.CharField(source = 'user.code_employee')
    class Meta:
        model = Payroll
        exclude = ('user', 'id')
