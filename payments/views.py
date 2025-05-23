from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from materials.models import Course
from . import services
from .models import StripePayment

class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product = services.create_product(name=request.data['name'])
        return Response(product, status=status.HTTP_201_CREATED)

class CreatePriceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount_in_cents = int(float(request.data['amount']) * 100)
        price = services.create_price(
            product_id=request.data['product_id'],
            amount=amount_in_cents
        )
        return Response(price, status=status.HTTP_201_CREATED)

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            course = Course.objects.get(id=request.data['course_id'])
            price_id = request.data['price_id']
            session = services.create_session(
                price_id=price_id,
                success_url=request.data.get('success_url', 'https://example.com/success'),
                cancel_url=request.data.get('cancel_url', 'https://example.com/cancel')
            )
            payment = services.create_payment_record(
                user=request.user,
                course=course,
                stripe_product_id=request.data['product_id'],
                stripe_price_id=price_id,
                session_id=session.id,
                checkout_url=session.url,
                amount=float(request.data['amount'])
            )

            return Response({
                'checkout_url': session.url,
                'payment_id': payment.id
            }, status=status.HTTP_201_CREATED)
            
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class RetrieveSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = services.retrieve_session(session_id)
            return Response(session)
        except StripePayment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
