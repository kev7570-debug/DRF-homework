from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner']
        extra_kwargs = {
            'video_url': {'validators': [validate_youtube_url]},
        }


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()