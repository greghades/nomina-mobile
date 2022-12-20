from django.urls import path
from .views import LoginView, SignUpView,LogoutView, DeleteView,UpdateUser,ListUsers

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('delete/<int:pk>/', DeleteView.as_view()),
    path('update/<int:pk>/',UpdateUser.as_view()),
    path('listUsers/',ListUsers.as_view()),
]