from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsOwnerOrModeratorOrReadOnly, IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .paginators import CoursePagination, LessonPagination
from .tasks import send_course_update_email
from django.utils import timezone
from datetime import timedelta

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CoursePagination
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LessonPagination
    
    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        course = lesson.course
        # Проверка: если курс не обновлялся более 4 часов
        if timezone.now() - course.updated_at > timedelta(hours=4):
            subscribers = course.subscription_set.all()
            for sub in subscribers:
                send_course_update_email.delay(sub.user.email, course.title, lesson.title)

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class SubscriptionCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        if not self.request.user.is_authenticated:
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, course_id=course_id)

    def destroy(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        subscription = Subscription.objects.filter(user=request.user, course_id=course_id).first()
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)