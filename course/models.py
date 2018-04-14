from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(_('degree'), max_length=50, blank=True, null=True)
    salary = models.FloatField()


class Material(models.Model):
    text = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name="course_material", on_delete=models.CASCADE)


