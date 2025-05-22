from django.urls import path
from .views import CreateProductView, CreatePriceView, CreateCheckoutSessionView, RetrieveSessionView

urlpatterns = [
    path('create-product/', CreateProductView.as_view()),
    path('create-price/', CreatePriceView.as_view()),
    path('create-session/', CreateCheckoutSessionView.as_view()),
    path('retrieve-session/<str:session_id>/', RetrieveSessionView.as_view()),
] 