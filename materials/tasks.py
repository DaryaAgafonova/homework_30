from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

def get_default_from_email():
    return getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')

@shared_task
def send_course_update_email(user_email, course_title, lesson_title):
    send_mail(
        subject=f'Обновление в курсе: {course_title}',
        message=f'В курсе "{course_title}" появился новый урок: "{lesson_title}"!',
        from_email=get_default_from_email(),
        recipient_list=[user_email],
        fail_silently=False,
    ) 