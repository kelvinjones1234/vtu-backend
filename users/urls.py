from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
  UserDetail,
  MyTokenObtainPairView, 
  RegisterView, 
  TransferView, 
  NotificationListView,
  WalletDetailView,
  FundWalletView,
  PasswordResetRequestView,
  PasswordResetView
)
 
urlpatterns = [
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('authentication/register/', RegisterView.as_view(), name='register'),

  # transfer and notifications
  path('wallet/<str:wallet_name__username>/', WalletDetailView.as_view(), name='wallet_detail'),
  path('fund-wallet/<str:wallet_name__username>/', FundWalletView.as_view(), name='wallet_detail'),
  path('transfer/', TransferView.as_view(), name='transfer'),
  path('notifications/', NotificationListView.as_view(), name='notifications'),

  # user profile display and update endpoint
  path('user/', UserDetail.as_view(), name='user-detail'),

  #reset password
  path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
  path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='password_reset_confirm'),

]