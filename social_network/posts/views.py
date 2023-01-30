# pylint: disable=E1101, W0613, W0707
import datetime
import jwt
from rest_framework.exceptions import ( AuthenticationFailed, NotFound,
                                        ValidationError )
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from .models import User, Posts, Likes, UserActivity


def handle_token(authorization_header):
    if not authorization_header:
        raise AuthenticationFailed('Unauthenticated User!')

    token = authorization_header[7:]
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated User!')

    return payload


class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        serializer = UserSerializer(data=model_to_dict(user))
        serializer.update(user)
        response = Response()

        response.data = {
            'jwt': token
        }

        return response


class PostCreationView(APIView):
    def post(self, request: Request) -> Response:
        authorization_header = request.headers.get('Authorization')

        payload = handle_token(authorization_header)

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found!")

        post_data = request.data.copy()
        post_data['user'] = user.id

        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PostsView(APIView):
    def get(self, request: Request) -> Response:
        authorization_header = request.headers.get('Authorization')
        handle_token(authorization_header)

        posts = Posts.objects.all().values()
        return Response(list(posts))

class LikesView(APIView):
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        authorization_header = request.headers.get('Authorization')

        payload = handle_token(authorization_header)

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found!")

        post_id = kwargs.get('post_id')
        action_type = kwargs.get('action_type')

        post = Posts.objects.filter(id=post_id).first()

        if not post:
            raise NotFound(f'Post with id {post_id} not found!')

        if action_type not in ['like', 'unlike']:
            raise ValidationError(f'Action Type {action_type} not correct!')
        if Likes.objects.filter(user=user.id, post=post.id).first() \
             and action_type == "like":
            return Response("This post already liked by you.")

        if action_type == 'like':
            like_data = {
                'post': post.id,
                'user': user.id,
            }
            like_serializer = LikeSerializer(data=like_data)
            like_serializer.is_valid(raise_exception=True)
            like_serializer.save()

        elif action_type == 'unlike':
            like_obj = Likes.objects.filter(post=post.id, user=user.id).first()
            if like_obj:
                like_obj.delete()
            else:
                raise NotFound("You already unliked the post.")

        return Response(kwargs['post_id'])


class AnaliticsView(APIView):
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        authorization_header = request.headers.get('Authorization')

        payload = handle_token(authorization_header)

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found!")

        analitics_data = Likes.object.all()
        params_dict = {}
        if kwargs.get('date_from'):
            params_dict['from'] = kwargs.get('date_from')
        if kwargs.get('date_to'):
            params_dict['to'] = kwargs.get('date_to')

        try:
            for val in params_dict.values():
                datetime.datetime.strptime(val, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(
                "One of Query Parameter has incorrect format!"
            )
        for key, val in params_dict.items():
            if key == 'from':
                analitics_data = analitics_data.filter(
                    creation_dt__ge = val
                )
            if key == 'to':
                analitics_data = analitics_data.filter(
                    creation_dt__le = val
                )

        response = Response()
        response.data = {
            'like_count': analitics_data.count()
        }

        return Response()


class UserAnaliticsView(APIView):
    def get(self, request: Request) -> Response:
        authorization_header = request.headers.get('Authorization')

        payload = handle_token(authorization_header)

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found!")
        last_activity = UserActivity.objects.filter(user=user.id).order_by(
            '-action_dt').first()
        response = Response()
        response.data = {
            'last_login': user.last_login,
            'last_action': last_activity.action,
            'last_action_dt':last_activity.action_dt
        }

        return response
