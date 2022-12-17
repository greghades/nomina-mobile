from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Payroll
from .serializers import PayrollSerializer
# Create your views here.

class GetAllPayrollView(APIView):
    
    def get(self, request):
        queryset= Payroll.objects.all()
        print(queryset)
        serializer= PayrollSerializer(queryset, many=True)
        serialized_data= serializer.data
        return Response(serialized_data, status.HTTP_200_OK)

class GetDetailPayrollView(APIView):

      def get(self, request, pk):
        payroll= Payroll.objects.get(id=pk)
        data= request.data              
        serializer = PayrollSerializer(instance=payroll, data=data)
        if serializer.is_valid():
            serializer.save()
        serialized_data= serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
