from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChangePasswordView,
    FollowViewSet,
    UsersViewSet,
    LogoutView,
    AccessTokenView
)

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe', FollowViewSet,
                   basename='follow')

urlpatterns = [
    path('auth/token/login/', AccessTokenView.as_view(), name='token'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
    path(
        'users/subscriptions/',
        FollowViewSet.as_view({'get': 'list'}),
        name='follow'),
    path(
        'users/set_password/',
        ChangePasswordView.as_view({'post': 'partial_update'}),
        name='password_update'),
    path('', include(router_v1.urls)),
]
