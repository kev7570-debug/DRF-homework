import re
from rest_framework import serializers


def validate_youtube_url(value):
    """
    Валидатор проверяет, что ссылка ведёт на youtube.com.
    """
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            'Разрешены только ссылки на youtube.com'
        )
    return value
