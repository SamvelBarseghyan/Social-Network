from django.urls import path
from .views import ( RegisterView, LoginView, PostCreationView,
                     LikesView, AnaliticsView, UserAnaliticsView )

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('post', PostCreationView.as_view(), name='post_creation'),
    path(
        'posts/<int:post_id>/action/<str:action_type>',
        LikesView.as_view(),
        name='like'
    ),
    path('analitics', AnaliticsView.as_view(), name='analitics'),
    path('user_statistics', UserAnaliticsView.as_view(), name='user_activity'),
]
