from django.urls import path
from accounts.views import RegisterUserView, VerifyUserEmail


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
]