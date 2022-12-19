from django.urls import path
from .views import GetDetailPayrollView, GetAllPayrollView

urlpatterns = [
    path('listar', GetAllPayrollView.as_view()),
    path('detalle/<int:pk>/', GetDetailPayrollView.as_view()),
]