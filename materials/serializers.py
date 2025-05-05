from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    owner_email = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    owner_email = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()