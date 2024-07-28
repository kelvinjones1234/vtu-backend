from django.shortcuts import render
from.serializers import (
    MyTokenObtainPairSerializer, 
    RegisterSerializer, 
    NotificationSerializer, 
    WalletSerializer, 
    TransferSerializer,
    UserSerializer,
    FundWalletSerializer,
    PasswordResetSerializer,
    PasswordResetRequestSerializer
    )
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Notification, Wallet, User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user

            if not sender.is_authenticated:
                raise PermissionDenied("User is not authenticated")

            recipient_phone_number = serializer.validated_data['phone_number']
            amount = serializer.validated_data['amount']
            transaction_pin = serializer.validated_data['transaction_pin']

            if not transaction_pin == sender.transaction_pin:
                return Response({'error': 'Invalid transaction pin'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = User.objects.get(phone_number=recipient_phone_number)
            except User.DoesNotExist:
                return Response({'error': 'Recipient does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if sender.wallet.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

            sender.wallet.balance -= amount
            recipient.wallet.balance += amount
            sender.wallet.save()
            recipient.wallet.save()

            Notification.objects.create(user=recipient, message=f"You have received {amount} credits from {sender.username}")
            Notification.objects.create(user=sender, message=f"You have sent {amount} credits to {recipient.username}")

            return Response({
                'success': 'Transfer completed',
                'balance': sender.wallet.balance  # Include the updated balance
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class WalletDetailView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'wallet_name__username'

class FundWalletView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = FundWalletSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        username = self.kwargs.get('wallet_name__username')
        return get_object_or_404(Wallet, wallet_name__username=username)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user 

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f'http://localhost:8000/reset-password/{uid}/{token}/'
                return Response({'reset_link': reset_link}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))
            try:
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                    return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)