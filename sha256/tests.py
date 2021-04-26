from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Hash

User = get_user_model()


class HashModelTestUnit(TestCase):
    """testing Hash model"""
    def test_creating_hash_model(self):
        text = 'hello'
        hash = '2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824'
        user = User.objects.create_user(
            username='hiwa',
            password='hiwa_asdf'
        )
        hash_obj = Hash.objects.create(
            text=text,
            hash=hash,
            user=user
        )
        self.assertEqual(Hash.objects.get(hash=hash).text, text)
