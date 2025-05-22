from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='users/avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, related_name='payments', verbose_name='Оплаченный курс', null=True, blank=True)
    lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, related_name='payments', verbose_name='Оплаченный урок', null=True, blank=True)
    amount = models.DecimalField('Сумма оплаты', max_digits=10, decimal_places=2)
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_METHOD_CHOICES)
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']
    
    def __str__(self):
        paid_item = self.course.title if self.course else (self.lesson.title if self.lesson else "Неизвестный товар")
        return f"Платеж {self.user.email} за {paid_item} - {self.amount} руб."
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.course and self.lesson:
            raise ValidationError('Нельзя указать одновременно и курс, и урок')
        if not self.course and not self.lesson:
            raise ValidationError('Необходимо указать либо курс, либо урок')