from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'', UserViewSet)

payments_router = DefaultRouter()
payments_router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('', include(router.urls)),
    path('payments/', include(payments_router.urls)),
]