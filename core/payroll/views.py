from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Payroll
from .serializers import PayrollSerializer

# Create your views here.

class GetAllPayrollView(APIView):
   
    def post(self, request):
      
        user_id = request.data.get("id", None)
        queryset= Payroll.objects.filter(user=user_id)
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
