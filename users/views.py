from rest_framework import viewsets, filters, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
from .models import User, Payment
from .serializers import (
    UserSerializer, PaymentSerializer, UserPaymentHistorySerializer,
    UserRegistrationSerializer, UserPublicSerializer
)
from .filters import PaymentFilter
from .permissions import IsOwnerOrModeratorOrReadOnly, IsOwnerOrAdmin

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            user_id = self.kwargs.get('pk')
            if str(self.request.user.id) == user_id or self.request.user.is_staff:
                if self.request.query_params.get('with_payments', False):
                    return UserPaymentHistorySerializer
                return UserSerializer
            else:
                return UserPublicSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']  
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Модераторы').exists():
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)