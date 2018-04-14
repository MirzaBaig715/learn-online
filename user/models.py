from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from location.models import City, Country
from course.models import Course
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('email is required')
        email = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Role:
        TUTOR = 1
        STUDENT = 2
        ADMIN = 3

        Choices = (
            (TUTOR, 'tutor'),
            (STUDENT, 'student'),
            (ADMIN, 'Admin'),
        )

    class Gender:
        UNKNOWN = 3
        MALE = 1
        FEMALE = 2

        Choices = (
            (UNKNOWN, 'Unknown'),
            (FEMALE, 'Female'),
            (MALE, 'Male')
        )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    created_at = models.DateTimeField(_('date joined'), default=timezone.now,
                                      help_text=_('Designates when the user joined the system.'))
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into admin site.'))
    is_active = models.BooleanField(_('active'), default=True)
    gender = models.IntegerField(_('gender'), choices=Gender.Choices, default=Gender.UNKNOWN)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255, null=True, blank=True)
    dob = models.DateField(_('date of birth'), null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=Role.Choices, default=Role.STUDENT)
    country = models.ForeignKey(Country, related_name="user_country", null=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, related_name="user_city", null=True, on_delete=models.DO_NOTHING)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):

        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):

        # Returns the short name for the user.
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):

        # Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Tutor(models.Model):
    user = models.OneToOneField(User, related_name='tutor_user', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(_('degree'), max_length=50, blank=True, null=True)
    salary = models.FloatField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = _("tutor")
        verbose_name_plural = _("tutors")

    # @property
    # def username(self):
    #     return self.user.first_name


class Student(models.Model):
    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name="student_courses", blank=True)

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    # @property
    # def username(self):
    #     return self.user.first_name
     

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        if instance.role == User.Role.TUTOR:
            Tutor.objects.create(user=instance)
            instance.tutor_user.save()
        elif instance.role == User.Role.STUDENT:
            Student.objects.create(user=instance)
            instance.student_user.save()
