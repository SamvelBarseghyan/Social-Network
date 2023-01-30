from django.utils import timezone
from rest_framework import serializers
from .models import User, Posts, Likes, UserActivity



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def update(self, instance: User, validated_data: dict = None) -> None:
        instance.last_login = timezone.now()
        instance.save()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'content', 'user', 'creation_dt']

    def create(self, validated_data: dict) -> Posts:
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['post', 'user', 'creation_dt']

    def create(self, validated_data: dict) -> Likes:
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user', 'action']

    def create(self, validated_data: dict) -> UserActivity:
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance
