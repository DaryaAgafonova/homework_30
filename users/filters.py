import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    payment_date_after = django_filters.DateTimeFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_before = django_filters.DateTimeFilter(field_name='payment_date', lookup_expr='lte')
    
    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],
            'lesson': ['exact'],
            'payment_method': ['exact'],
            'user': ['exact'],
            'amount': ['gte', 'lte'],
        }