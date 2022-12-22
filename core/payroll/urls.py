from django.urls import path
from .views import GetAllPayrollView

urlpatterns = [
    path('list/<int:pk>/', GetAllPayrollView.as_view()),
]