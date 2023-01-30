from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from .models import User
from .serializers import UserSerializer
from .views import RegisterView, LoginView

class RegistrationViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_registration_view(self):
        data = {
            'name': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@test.test',
        }
        request = self.factory.post(reverse('register'), data)
        view = RegisterView.as_view()
        response = view(request)        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@test.test')
        self.assertEqual(User.objects.get().name, 'testuser')


class LoginViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_login_view(self):
        data = {
            'name': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@test.test',
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        request_data = {
            'email': 'testuser@test.test',
            'password': 'testpassword',
        }
        request = self.factory.post(reverse('login'), request_data)
        view = LoginView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.data)
        self.assertIn('jwt', response.data)
        self.assertIsNotNone(User.objects.get().last_login)
