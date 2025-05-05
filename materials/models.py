from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField('Название', max_length=255)
    preview = models.ImageField('Превью', upload_to='courses/previews/', null=True, blank=True)
    description = models.TextField('Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_courses', verbose_name='Владелец')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    preview = models.ImageField('Превью', upload_to='lessons/previews/', null=True, blank=True)
    video_url = models.URLField('Ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_lessons', verbose_name='Владелец')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'id']

    def __str__(self):
        return f"{self.course.title} - {self.title}"