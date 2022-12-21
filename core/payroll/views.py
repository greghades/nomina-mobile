from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Payroll
from .serializers import PayrollSerializer
from .messages.responseErrors import NOT_FOUND_PAYROLL
from authentication.models import CustomUser
from core.settings import STATIC_ROOT
# Create your views here.

class GetAllPayrollView(APIView):
   
    def get(self, request,pk):
        queryset= Payroll.objects.filter(user=pk)
        serializer= PayrollSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class GetDetailPayrollView(APIView):

      def get(self, request, pk):
        payroll= Payroll.objects.filter(id=pk).first()
        if payroll:
            serializer = PayrollSerializer(payroll, many=False)
            # if serializer.is_valid():
            #     serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message":"No se ha encontrado el usuario"}, status=status.HTTP_400_BAD_REQUEST)

class DownloadPayrollPdf(generics.GenericAPIView):
    
    serializer_class = PayrollSerializer

    def post(self,request):

        code_employee = request.data.get("code_employee", None)
        payment_date = request.data.get("payment_date", None)
       
        if code_employee is not None and payment_date is not None:
            user = CustomUser.objects.get(code_employee=code_employee)
            payroll = Payroll.objects.filter(user=user.id,payment_date=payment_date).first()
            
    
            rspn = {
                   'url_pdf':STATIC_ROOT + '/'+user.code_employee+'/'+user.code_employee+'-'+str(payroll.payment_date)+'.pdf',
                   
            }
            return Response( rspn, status=status.HTTP_200_OK)
        else:
            return Response(NOT_FOUND_PAYROLL, status=status.HTTP_404_NOT_FOUND)