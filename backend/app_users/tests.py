from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .views import *
from .serializers import *


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """Тест регистрации с несовпадающими паролями"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'differentpassword'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_registration_existing_email(self):
        """Тест регистрации с уже существующим email"""
        # Создаем пользователя
        User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='password123'
        )
        
        # Пытаемся зарегистрировать пользователя с тем же email
        data = {
            'email': 'existing@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, 400)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpassword123'
        )

    def test_user_login_success(self):
        """Тест успешного входа пользователя"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/users/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/users/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_nonexistent_user(self):
        """Тест входа несуществующего пользователя"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/users/login/', data, format='json')
        self.assertEqual(response.status_code, 400)


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpassword123'
        )
        # Получаем токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_me_view_authenticated(self):
        """Тест представления me с аутентификацией"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_me_view_unauthenticated(self):
        """Тест представления me без аутентификации"""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, 401)


class RegisterSerializerTestCase(TestCase):
    def test_register_serializer_valid_data(self):
        """Тест валидного сериализатора регистрации"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid_email(self):
        """Тест невалидного email в сериализаторе регистрации"""
        data = {
            'email': 'invalid-email',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_register_serializer_password_mismatch(self):
        """Тест несовпадения паролей в сериализаторе регистрации"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'differentpassword'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpassword123'
        )

    def test_login_serializer_valid_data(self):
        """Тест валидного сериализатора входа"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validate(data)
        self.assertIn('user', validated_data)

    def test_login_serializer_invalid_credentials(self):
        """Тест невалидных учетных данных в сериализаторе входа"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        serializer = LoginSerializer(data=data)
        # Валидация может не пройти из-за неверных учетных данных
        # Проверим, что validate вызывает исключение
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)