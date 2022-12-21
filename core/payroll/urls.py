from django.urls import path
from .views import GetDetailPayrollView, GetAllPayrollView,DownloadPayrollPdf

urlpatterns = [
    path('list/<int:pk>/', GetAllPayrollView.as_view()),
    path('detalle/<int:pk>/', GetDetailPayrollView.as_view()),
    path('donwload/',DownloadPayrollPdf.as_view()),
]