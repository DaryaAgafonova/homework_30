from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на YouTube
    """
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_regex, value):
        raise ValidationError(
            _('%(value)s не является ссылкой на YouTube'),
            params={'value': value},
        ) 