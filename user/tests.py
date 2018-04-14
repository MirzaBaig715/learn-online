from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tutor

User = get_user_model()


class TestTutorModel(TestCase):
    def test_profile_creation(self):
        # New user created
        user = User.objects.create(
            email="test@gmail.com",
            password="password123"
        )
        # Check that a Use instance has been crated
        self.assertIsInstance(user.tutor_user, Tutor)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.tutor_user, Tutor)