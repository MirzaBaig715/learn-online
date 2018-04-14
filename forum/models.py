from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course
from django.utils import timezone

User = get_user_model()


class Topic(models.Model):
    subject = models.CharField(max_length=20)
    topic_message = models.TextField(max_length=1000)
    user = models.ForeignKey(User, related_name='user_topics', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='course_topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    slug = models.SlugField(unique=True)


class Comment(models.Model):
    message = models.TextField()
    author = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    topic = models.ForeignKey(Topic, related_name='topic_comments', on_delete=models.CASCADE)
