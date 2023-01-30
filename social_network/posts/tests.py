
# pylint: disable=E1101
from django.test import TestCase
from .models import User
from .serializers import UserSerializer, UserActivitySerializer


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@test.test',
            password='testpassword',
            name='TestUser'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'email', 'name'])

    def test_user_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], 'testuser@test.test')
        self.assertEqual(data['name'], 'TestUser')

    def test_valid_data(self):
        data = {
            'email': 'testuser2@test.test',
            'password': 'testpassword2',
            'name': 'TestUser2'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_update_function(self):
        serializer = UserSerializer(instance=self.user)
        serializer.update(instance=self.user)
        self.assertIsNotNone(self.user.last_login)


class UserActivitySerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@test.test',
            password='testpassword',
            name='TestUser'
        )

    def test_valid_data(self):
        data = {
            'user': self.user.id,
            'action': "like"
        }
        val_data = {
            'user': self.user,
            'action': 'like'
        }
        serializer = UserActivitySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, val_data)
