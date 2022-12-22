from django.urls import path
from .views import LoginView, ResetPasswordView, SendCodeResetPassword, SignUpView,LogoutView, DeleteView,UpdateUser,ListUsers, ValidationCodeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('delete/<int:pk>/', DeleteView.as_view()),
    path('update/<int:pk>/',UpdateUser.as_view()),
    path('listUsers/',ListUsers.as_view()),
    path('passwordReset/',SendCodeResetPassword.as_view()),
    path('validateCode/',ValidationCodeView.as_view()),
    path('resetPasswordView/',ResetPasswordView.as_view())
]