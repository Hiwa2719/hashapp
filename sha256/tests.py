from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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

    def setUp(self) ->None:
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.login_url = reverse('login')
        self.register_url = reverse('register')

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

    def test_login_view_get_ajax(self):
        """testing login a user"""
        response = self.client.get(self.login_url, **self.ajax_header)
        self.login_test(response)

    def login_test(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].__class__, AuthenticationForm)

    def test_login_view_get(self):
        """test accessing login view with template"""
        response = self.client.get(self.login_url)
        self.login_test(response)
        self.assertTemplateUsed(response=response, template_name='registration/login.html')

    def test_login_view_post_ajax(self):
        """test user authentication"""
        data = {
            'username': 'hiwa@gamil.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(**data)
        response = self.client.post(self.login_url, data=data, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('authentication successful', str(response.content, encoding='utf-8'))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.id)

    def test_login_view_post(self):
        """test post while using template"""
        data = {
            'username': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(**data)
        response = self.client.post(self.login_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('account'))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.id)

    def test_login_view_wrong_input_ajax(self):
        """testing login view with wrong password"""
        data = {
            'username': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(
            **data
        )
        response = self.client.post(self.login_url,
                                    data={'username': 'hiwa@gmail.com', 'password': 'hiwa'},
                                    **self.ajax_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a correct username and password', str(response.content, encoding='utf-8'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_view_wrong_input(self):
        """test login view with template with wrong input"""
        data = {
            'username': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(
            **data
        )
        response = self.client.post(self.login_url,
                                    data={'username': 'hiwa@gmail.com', 'password': 'hiwa'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertTemplateUsed(response, template_name='registration/login.html')
        self.assertTrue(response.context.get('form').errors)

    def test_register_view_ajax(self):
        """test getting register view in ajax mode"""
        response = self.client.get(self.register_url, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context.get('form').__class__, UserCreationForm)

    def test_register_view(self):
        """test register view while using template"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_view_post_ajax(self):
        """test registering a user"""
        data = {
            'username': 'hiwa@gmail.com',
            'password1': 'hiwa_asdf',
            'password2': 'hiwa_asdf'
        }
        response = self.client.post(self.register_url, data=data, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'msg': 'user created'})
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_view_post(self):
        """test registering a user"""
        data = {
            'username': 'hiwa@gmail.com',
            'password1': 'hiwa_asdf',
            'password2': 'hiwa_asdf'
        }
        response = self.client.post(self.register_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request.get('PATH_INFO'), '/account/')
        self.assertIn('_auth_user_id', self.client.session)

    def test_registering_with_wrong_input_ajax(self):
        """test registering with short password in ajax mode"""
        data = {
            'username': 'hiwa@gmail.com',
            'password1': 'hiwa',
            'password2': 'hiwa'
        }
        response = self.client.post(self.register_url, data=data, **self.ajax_header)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context.get('form').errors)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registering_with_wrong_input(self):
        """test registering with short password"""
        data = {
            'username': 'hiwa@gmail.com',
            'password1': 'hiwa',
            'password2': 'hiwa'
        }
        response = self.client.post(self.register_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('form').errors)
        self.assertNotIn('_auth_user_id', self.client.session)


class PrivateUniteTests(TestCase):

    def setUp(self) -> None:
        data = {'username': 'hiwa@gmail.com', 'password': 'hiwa_asdf'}
        self.user = User.objects.create_user(**data)
        self.client.force_login(self.user)
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.account_url = reverse('account')

    def test_log_out(self):
        """testing logout user"""
        url = reverse('logout')
        response = self.client.get(url, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(response.json(), {'msg': 'logged out'})

    def test_getting_account_url(self):
        """test accessing account url"""
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sha256/account.html')

    def test_delete_account_get(self):
        """test delete account"""
        url = reverse('delete-account', kwargs={'pk': self.user.id})
        response = self.client.get(url, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Are you sure to delete this account?', str(response.content, encoding='utf-8'))

    def test_delete_account_post(self):
        """test finalizing the deletion"""
        url = reverse('delete-account', kwargs={'pk': self.user.id})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)
        self.assertURLEqual(response.request.get('PATH_INFO'), '/')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_change_password_get(self):
        """test changing pass"""
        url = reverse('pass-change')
        response = self.client.get(url, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.json())
        self.assertIn('old_password', response.json().get('form'))

    def test_change_password_post(self):
        """test changing password with post method"""
        url = reverse('pass-change')
        data = {
            'old_password': 'hiwa_asdf',
            'new_password1': 'asdf_hiwa',
            'new_password2': 'asdf_hiwa'
        }
        response = self.client.post(url, data=data, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'msg': 'password successfully changed'})
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('asdf_hiwa'))

    def test_change_password_post_wrong_input(self):
        """sending wrong inputs to password change"""
        url = reverse('pass-change')
        data = {
            'old_password': 'hiwa_asdf',
            'new_password1': 'hiwa',
            'new_password2': 'hiwa'
        }
        response = self.client.post(url , data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password is too short', str(response.content, encoding='utf-8'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('hiwa_asdf'))

    def test_display_save_text_hash(self):
        """test getting saved text/hashes"""
        Hash.objects.create(user=self.user,
                            text='hello',
                            hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        url = reverse('sha256:hash-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content_str = str(response.content, encoding='utf-8')
        self.assertIn('hello', content_str)
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', content_str)

    def test_display_saved_text_hash_with_query(self):
        """filtering down the saved texts"""
        Hash.objects.create(user=self.user,
                            text='hello',
                            hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        Hash.objects.create(user=self.user,
                            text='world',
                            hash='486EA46224D1BB4FB680F34F7C9AD96A8F24EC88BE73EA8E5A6C65260E9CB8A7')
        url = reverse('sha256:hash-list')
        response = self.client.get(url + '?q=hello')
        self.assertEqual(response.status_code, 200)
        content_str = str(response.content, encoding='utf-8')
        self.assertIn('hello', content_str)
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', content_str)
        self.assertNotIn('486EA46224D1BB4FB680F34F7C9AD96A8F24EC88BE73EA8E5A6C65260E9CB8A7', content_str)
        self.assertNotIn('world', content_str)

    def test_display_saved_text_hash_with_wrong_query(self):
        """searing for unavailable key """
        url = reverse('sha256:hash-list')
        response = self.client.get(url + '?q=hello')
        content_str = str(response.content, encoding='utf-8')
        self.assertIn('No data', content_str)

    def test_save_hash(self):
        """saving entered text/hash"""
        url = reverse('sha256:save-text-hash')
        response = self.client.post(url,
                                    data={'text': 'hello'})
        self.assertEqual(response.status_code, 201)
        queryset = Hash.objects.filter(text='hello')
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().hash, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
