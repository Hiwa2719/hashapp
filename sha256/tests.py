import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Hash
from .views import IndexView

User = get_user_model()


class HashModelTestUnit(TestCase):
    """testing Hash model"""
    def test_creating_hash_model(self):
        text = 'hello'
        hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
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


class PublicViewUnitTest(TestCase):
    """testing index view"""

    def test_getting_index_view(self):
        """accessing index view"""
        url = reverse('sha256:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        # self.assertContains(response, 'please enter your text here')
        self.assertTemplateUsed(response, 'sha256/index.html')
        self.assertEqual(response.resolver_match.func.__name__, IndexView.as_view().__name__)

    def test_posting_to_hash_gen(self):
        """test posting text to index view and getting back the hash result"""
        url = reverse('sha256:hash-gen')
        response = self.client.post(url, data={'text': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'hash': '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'})

    def test_posting_to_hash_gen_wrong_data(self):
        """test posting empty text to hash gen"""
        url = reverse('sha256:hash-gen')
        response = self.client.post(url, data={'text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'msg': 'invalid text'})

    def test_login_view_get(self):
        """testing login a user"""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_login_view_post(self):
        """test user authentication"""
        data = {
            'username': 'hiwa@gamil.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(**data)
        url = reverse('login')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'authentication successful')

    def test_login_view_wrong_input(self):
        """testing login view with wrong password"""
        data = {
            'username': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(
            **data
        )
        url = reverse('login')
        response = self.client.post(url, data={'username': 'hiwa@gmail.com', 'password': 'hiwa'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a correct username and password', str(response.content, encoding='utf-8'))
