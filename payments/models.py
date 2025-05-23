from django.db import models
from django.conf import settings
from materials.models import Course

class StripePayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stripe_payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='stripe_payments')
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    checkout_url = models.URLField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stripe Payment'
        verbose_name_plural = 'Stripe Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Stripe Payment {self.id} - {self.user.email} - {self.course.name}"
