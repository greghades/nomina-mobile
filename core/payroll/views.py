from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Payroll
from .serializers import PayrollSerializer
from authentication.models import CustomUser
# Create your views here.

class GetAllPayrollView(APIView):
   
    def get(self, request,pk):
      
        user = CustomUser.objects.get(id=pk)
        payrolls = Payroll.objects.filter(user=pk)
        rspn = []
        for payroll in  payrolls:
           rspn.append( {
                    'code_employee':user.code_employee,
                    'payment_date':payroll.payment_date,
                    'url_pdf':'http://3.95.16.122/static/nomina-mobile/payrolls' + '/'+user.code_employee+'/'+user.code_employee+'-'+str(payroll.payment_date)+'.pdf',
                   
                })
        
        return Response( rspn, status=status.HTTP_200_OK)
