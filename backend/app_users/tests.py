from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .logic import change_password, change_email, archive_user, update_avatar

User = get_user_model()


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'username': 'testuser'
        }

    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя"""
        response = self.client.post(reverse('register'), self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """Тест регистрации с несовпадающими паролями"""
        data = self.user_data.copy()
        data['password_confirm'] = 'differentpassword'
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_registration_existing_email(self):
        """Тест регистрации с существующим email"""
        # Создаем пользователя
        User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='password123'
        )
        
        # Пытаемся зарегистрировать пользователя с тем же email
        data = self.user_data.copy()
        data['email'] = 'existing@example.com'
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_success(self):
        """Тест успешного входа пользователя"""
        # Сначала регистрируем пользователя
        self.client.post(reverse('register'), self.user_data, format='json')
        
        # Затем пробуем войти
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        # Сначала регистрируем пользователя
        self.client.post(reverse('register'), self.user_data, format='json')
        
        # Пробуем войти с неверным паролем
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_me_view_authenticated(self):
        """Тест представления me с аутентификацией"""
        # Регистрируем и аутентифицируем пользователя
        self.client.post(reverse('register'), self.user_data, format='json')
        login_response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }, format='json')
        
        # Устанавливаем токен аутентификации
        token = login_response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        response = self.client.get(reverse('me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_profile_authenticated(self):
        """Тест получения профиля с аутентификацией"""
        response = self.client.get(reverse('get_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_change_password_success(self):
        """Тест успешной смены пароля"""
        change_pwd_data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123'
        }
        response = self.client.put(reverse('change_password'), change_pwd_data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что новый пароль работает
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_wrong_old_password(self):
        """Тест смены пароля с неправильным старым паролем"""
        change_pwd_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123'
        }
        response = self.client.put(reverse('change_password'), change_pwd_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_change_password_mismatch(self):
        """Тест смены пароля с несовпадающими новыми паролями"""
        change_pwd_data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword123',
            'confirm_new_password': 'differentpassword'
        }
        response = self.client.put(reverse('change_password'), change_pwd_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_change_email_success(self):
        """Тест успешной смены email"""
        change_email_data = {
            'new_email': 'newemail@example.com'
        }
        response = self.client.put(reverse('change_email'), change_email_data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что email изменился
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_change_email_duplicate(self):
        """Тест смены email на уже существующий"""
        # Создаем другого пользователя
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='password123'
        )
        
        change_email_data = {
            'new_email': 'other@example.com'
        }
        response = self.client.put(reverse('change_email'), change_email_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_avatar(self):
        """Тест обновления аватара"""
        # Создаем фиктивный файл изображения
        avatar_file = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        response = self.client.put(reverse('update_avatar'), {'avatar': avatar_file})
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что аватар обновился
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.avatar)

    def test_archive_account(self):
        """Тест архивации аккаунта"""
        response = self.client.delete(reverse('archive_account'))
        self.assertEqual(response.status_code, 204)
        
        # Проверяем, что пользователь архивирован (неактивен)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)



class UserLogicTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)

    def test_change_password_logic(self):
        """Тест логики смены пароля"""
        success = change_password(self.user, 'testpassword123', 'newpassword123', 'newpassword123')
        self.assertTrue(success)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_email_logic(self):
        """Тест логики смены email"""
        success = change_email(self.user, 'newemail@example.com')
        self.assertTrue(success)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_archive_user_logic(self):
        """Тест логики архивации пользователя"""
        success = archive_user(self.user)
        self.assertTrue(success)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


    def test_update_avatar_logic(self):
        """Тест логики обновления аватара"""
        avatar_file = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

        success = update_avatar(self.user, avatar_file)
        self.assertTrue(success)
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.avatar)

