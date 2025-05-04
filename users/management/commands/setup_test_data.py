from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Payment
from materials.models import Course, Lesson
from decimal import Decimal
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Создание тестовых данных для проекта (пользователи, курсы, уроки, платежи)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаем создание тестовых данных...'))

        if User.objects.count() == 0:
            self.create_users()
        else:
            self.stdout.write(self.style.SUCCESS(f'Пользователи уже существуют: {User.objects.count()} шт.'))

        if Course.objects.count() == 0:
            self.create_courses()
        else:
            self.stdout.write(self.style.SUCCESS(f'Курсы уже существуют: {Course.objects.count()} шт.'))

        if Lesson.objects.count() == 0:
            self.create_lessons()
        else:
            self.stdout.write(self.style.SUCCESS(f'Уроки уже существуют: {Lesson.objects.count()} шт.'))

        self.create_payments()
        
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
    
    def create_users(self):
        test_users = [
            {
                'email': 'admin@example.com',
                'password': 'admin123',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'email': 'user1@example.com',
                'password': 'user123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+7 (999) 123-45-67',
                'city': 'Москва'
            },
            {
                'email': 'user2@example.com',
                'password': 'user123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+7 (999) 765-43-21',
                'city': 'Санкт-Петербург'
            }
        ]
        
        for user_data in test_users:
            if user_data.get('is_superuser'):
                User.objects.create_superuser(
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    phone=user_data.get('phone', ''),
                    city=user_data.get('city', '')
                )
            else:
                User.objects.create_user(
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    phone=user_data.get('phone', ''),
                    city=user_data.get('city', '')
                )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(test_users)} тестовых пользователей'))
    
    def create_courses(self):
        test_courses = [
            {
                'title': 'Python для начинающих',
                'description': 'Базовый курс по Python для новичков'
            },
            {
                'title': 'Django Framework',
                'description': 'Разработка веб-приложений на Django'
            },
            {
                'title': 'JavaScript Основы',
                'description': 'Основы JavaScript для фронтенд-разработки'
            },
            {
                'title': 'React.js',
                'description': 'Разработка современных UI с React'
            }
        ]
        
        for course_data in test_courses:
            Course.objects.create(
                title=course_data['title'],
                description=course_data['description']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(test_courses)} тестовых курсов'))
    
    def create_lessons(self):
        courses = Course.objects.all()
        lessons_created = 0
        
        for course in courses:
            num_lessons = random.randint(3, 6)
            
            for i in range(1, num_lessons + 1):
                Lesson.objects.create(
                    course=course,
                    title=f'Урок {i}: {course.title}',
                    description=f'Описание урока {i} для курса {course.title}',
                    video_url=f'https://example.com/video/{course.id}/{i}'
                )
                lessons_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Создано {lessons_created} тестовых уроков'))
    
    def create_payments(self):
        Payment.objects.all().delete()
        
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        
        payment_methods = ['cash', 'transfer']
        payments_created = 0

        for course in courses:
            for _ in range(random.randint(1, 3)): 
                user = random.choice(users)
                payment_date = datetime.now() - timedelta(days=random.randint(1, 30))
                amount = Decimal(str(random.randint(1000, 10000)))
                payment_method = random.choice(payment_methods)
                
                Payment.objects.create(
                    user=user,
                    payment_date=payment_date,
                    course=course,
                    amount=amount,
                    payment_method=payment_method
                )
                payments_created += 1
        
        for lesson in lessons:
            if random.random() < 0.3:
                user = random.choice(users)
                payment_date = datetime.now() - timedelta(days=random.randint(1, 30))
                amount = Decimal(str(random.randint(500, 2000)))
                payment_method = random.choice(payment_methods)
                
                Payment.objects.create(
                    user=user,
                    payment_date=payment_date,
                    lesson=lesson,
                    amount=amount,
                    payment_method=payment_method
                )
                payments_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Создано {payments_created} тестовых платежей'))