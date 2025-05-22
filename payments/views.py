from django.shortcuts import render
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)

class CreateProductView(APIView):
    def post(self, request):
        product = stripe.Product.create(name=request.data['name'])
        return Response(product, status=status.HTTP_201_CREATED)

class CreatePriceView(APIView):
    def post(self, request):
        price = stripe.Price.create(
            product=request.data['product_id'],
            unit_amount=request.data['amount'],
            currency='usd',
        )
        return Response(price, status=status.HTTP_201_CREATED)

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': request.data['price_id'],
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return Response({'checkout_url': session.url}, status=status.HTTP_201_CREATED)

class RetrieveSessionView(APIView):
    def get(self, request, session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        return Response(session)
