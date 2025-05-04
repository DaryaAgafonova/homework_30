from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Payment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')
    list_filter = ('payment_method', 'payment_date', 'course', 'lesson')
    search_fields = ('user__email', 'course__title', 'lesson__title')
    date_hierarchy = 'payment_date'