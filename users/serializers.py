from rest_framework import serializers
from .models import User, Payment
from materials.serializers import CourseSerializer, LessonSerializer
from django.contrib.auth.password_validation import validate_password

class PaymentSerializer(serializers.ModelSerializer):
    course_info = CourseSerializer(source='course', read_only=True)
    lesson_info = LessonSerializer(source='lesson', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserPaymentHistorySerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'payments']

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'phone', 'city', 'avatar']
        read_only_fields = ['id', 'email', 'first_name', 'phone', 'city', 'avatar']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'city']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user