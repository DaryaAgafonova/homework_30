from rest_framework import serializers
from .models import Course, Lesson, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['user', 'course', 'created_at']

class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'preview', 'video_url', 'owner', 'owner_email', 'created_at', 'updated_at']
        read_only_fields = ['owner']

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    owner_email = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'owner', 'created_at', 'updated_at', 'is_subscribed']
        read_only_fields = ['owner']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    owner_email = serializers.ReadOnlyField(source='owner.email')
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'owner', 'created_at', 'updated_at', 'lessons', 'lessons_count', 'owner_email', 'is_subscribed']
        read_only_fields = ['owner']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False