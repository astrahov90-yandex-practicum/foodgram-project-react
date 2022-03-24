from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import (AccessTokenSerializer, ChangePasswordSerializer,
                          FollowSerializer, UserSerializer)


class AccessTokenView(APIView):
    """
    Вьюсет получения токена авторизации.
    """
    permission_classes = [AllowAny, ]
    serializer_class = AccessTokenSerializer

    def post(self, request):
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)

        password = serializer.validated_data['password']
        if not user.check_password(password):
            return Response(
                {'password': 'Неверный пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key}, status=status.HTTP_200_OK)


class UsersViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Вьюсет пользователя для создания и чтения. CR.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'

    permission_classes = [AllowAny, ]

    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    Эндпоинт изменения пароля.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raiseExceptions=True)

        current_password = serializer.data.get('current_password')
        if not self.object.check_password(current_password):
            return Response({'current_password': ['Некорректный пароль.']},
                            status=status.HTTP_400_BAD_REQUEST)
        self.object.set_password(serializer.data.get('new_password'))
        self.object.save()
        response = {
            'status': 'Успешно',
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'Пароль успешно изменен',
            'data': []
        }

        return Response(response)


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет для класса Follow.
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    model = Follow
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, pk=author_id)

        if author == request.user:
            raise ValidationError('Самоподписывание недоступно')

        if request.user.follower.filter(author=author).exists():
            raise ValidationError('Повторная подписка недоступна')

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, pk=user_id)
        serializer.save(user=self.request.user, author=author)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, user_id):
        author = get_object_or_404(User, pk=user_id)

        instance = request.user.follower.filter(author=author)
        if not instance.exists():
            return Response(data='Пользователь не подписан',
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
