from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from materials.models import Course, Lesson, Subscription
from users.models import User

class LessonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_create_lesson(self):
        url = reverse('lesson-list-create')
        data = {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'video_link': 'https://www.youtube.com/watch?v=test',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, 'Test Lesson')

    def test_create_lesson_invalid_link(self):
        url = reverse('lesson-list-create')
        data = {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'video_link': 'https://invalid-link.com',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            title='Original Title',
            description='Original Description',
            course=self.course,
            owner=self.user
        )
        url = reverse('lesson-detail', args=[lesson.id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=lesson.id).title, 'Updated Title')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            course=self.course,
            owner=self.user
        )
        url = reverse('lesson-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

class SubscriptionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_create_subscription(self):
        url = reverse('course-subscribe', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )
        url = reverse('course-subscribe', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscription_status_in_response(self):
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])

        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed']) 