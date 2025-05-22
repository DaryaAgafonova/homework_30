from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('', include(router.urls)),
]